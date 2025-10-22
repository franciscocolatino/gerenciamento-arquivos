# Implementação do projeto "Gerenciamento de Arquivos Usando Lista Encadeada"
# Usa array para simular disco com 32 blocos.
# Cada bloco: 16 bits de dados (char armazenado como inteiro Unicode) + 16 bits de ponteiro (indice do próximo bloco)
# Ponteiro nulo: 65535 (max unsigned short)

from array import array

NULL_PTR = 0xFFFF  # 65535 - ponteiro nulo
DISK_BITS = 1024
BLOCK_SIZE_BITS = 32
NUM_BLOCKS = DISK_BITS // BLOCK_SIZE_BITS  # 32
# Usaremos dois arrays 'H' (unsigned short) de tamanho NUM_BLOCKS:
# data_array: armazena valor inteiro do caractere (ord), 0 = vazio
# ptr_array: armazena índice do próximo bloco ou NULL_PTR

class FileSystem:
    def __init__(self):
        self.data = array('H', [0] * NUM_BLOCKS)   # cada posição guarda 16 bits de dados (ord do char)
        self.ptr  = array('H', [NULL_PTR] * NUM_BLOCKS)  # ponteiros

        for i in range(NUM_BLOCKS - 1):
            self.ptr[i] = i + 1
        self.ptr[NUM_BLOCKS - 1] = NULL_PTR
        self.free_head = 0  # posição do primeiro bloco livre
        self.free_count = NUM_BLOCKS
        # tabela de diretório: map nome -> inicio_do_arquivo (índice do bloco)
        self.directory = {} 
    
    # função auxiliar: aloca n blocos (se possível) e retorna lista de índices alocados (na ordem)
    def _allocate_blocks(self, n):
        if n <= 0:
            return []
        if self.free_count < n:
            return None 
        allocated = []
        for _ in range(n):
            block = self.free_head
            if block == NULL_PTR:
                # erro inesperado
                return None
            # avança free_head para próximo livre
            self.free_head = self.ptr[block]
            self.ptr[block] = NULL_PTR
            allocated.append(block)
            self.free_count -= 1
        return allocated
    
    # função auxiliar: libera uma lista encadeada de blocos (a partir do primeiro)
    # ao liberar, nós "encaixamos" essa cadeia no início da lista livre
    def _free_chain(self, start_block):
        if start_block == NULL_PTR:
            return
        cur = start_block
        cnt = 0
        while cur != NULL_PTR:
            nxt = self.ptr[cur]
            cur = nxt
            cnt += 1
        # agora cur == NULL_PTR e cnt = tamanho da cadeia
        # ligar o último bloco liberado (que atualmente tem ptr = NULL_PTR) ao free_head
        # para isso precisamos localizar o último bloco real: percorremos novamente
        cur = start_block
        prev = None
        while cur != NULL_PTR:
            prev = cur
            cur = self.ptr[cur]
        # prev é o último bloco real (poderia ser None se start_block fosse NULL_PTR)
        if prev is not None:
            # ligar prev.ptr ao free_head
            self.ptr[prev] = self.free_head
            # atualizar free_head para start_block
            self.free_head = start_block
            # atualizar contagem
            self.free_count += cnt
    
    # cria um arquivo com nome (<=4 chars) e conteúdo (string)
    def create_file(self, name, content):
        name = str(name)
        if len(name) > 4:
            print(f"[ERRO] Nome '{name}' possui mais de 4 caracteres permitidos.")
            return False
        if name in self.directory:
            print(f"[ERRO] Já existe arquivo com nome '{name}'.")
            return False
        # cada caractere ocupa 1 bloco (conforme enunciado)
        required = len(content)
        if required == 0:
            # criar arquivo vazio: não aloca blocos; registramos inicio como NULL_PTR
            self.directory[name] = NULL_PTR
            print(f"[INFO] Arquivo '{name}' criado (vazio).")
            return True
        if self.free_count < required:
            print(f"[ERRO] Memória insuficiente para armazenar '{name}' (precisa de {required} blocos, "
                  f"livres: {self.free_count}).")
            return False
        # alocar blocos
        allocated = self._allocate_blocks(required)
        if allocated is None:
            print(f"[ERRO] Falha na alocação de blocos para '{name}'.")
            return False
        # preencher dados e encadear
        for i, ch in enumerate(content):
            blk = allocated[i]
            # armazenar ord(ch) no bloco
            code = ord(ch)
            if code > 0xFFFF:
                print(f"[AVISO] Caractere '{ch}' tem ord() > 65535; truncando para 16 bits.")
                code = code & 0xFFFF
            self.data[blk] = code
            # ponteiro para próximo bloco ou NULL_PTR se for o último
            if i < required - 1:
                self.ptr[blk] = allocated[i + 1]
            else:
                self.ptr[blk] = NULL_PTR
        # adicionar à diretório
        self.directory[name] = allocated[0]
        print(f"[OK] Arquivo '{name}' criado com {required} bloco(s). Início em {allocated[0]}.")
        return True
    
    # lê (retorna) o conteúdo do arquivo (string) e imprime; se arquivo não existe, avisa
    def read_file(self, name):
        if name not in self.directory:
            print(f"[ERRO] Arquivo '{name}' não encontrado.")
            return None
        start = self.directory[name]
        if start == NULL_PTR:
            print(f"[INFO] Arquivo '{name}' está vazio.")
            return ""
        cur = start
        chars = []
        visited = set()
        while cur != NULL_PTR:
            if cur in visited:
                print("[ERRO] Loop detectado na cadeia do arquivo! Corrupção.")
                break
            visited.add(cur)
            code = self.data[cur]
            # se código 0, interpretamos como caractere nulo / vazio
            ch = chr(code) if code != 0 else '\u0000'
            chars.append(ch)
            cur = self.ptr[cur]
        result = ''.join(chars)
        print(f"[LEITURA] '{name}': {result}")
        return result
    
    # exclui arquivo: remove entrada de diretório e libera blocos (se houver)
    def delete_file(self, name):
        if name not in self.directory:
            print(f"[ERRO] Arquivo '{name}' não encontrado.")
            return False
        start = self.directory.pop(name)
        if start == NULL_PTR:
            print(f"[OK] Arquivo '{name}' (vazio) removido.")
            return True
        # antes de ligar ao free list, limpamos os dados (opcional)
        cur = start
        count = 0
        while cur != NULL_PTR:
            self.data[cur] = 0
            nxt = self.ptr[cur]
            # deixar ptr cur como está — será reaproveitado quando ligado à free list
            cur = nxt
            count += 1
        # ligar cadeia liberada ao início da free list
        # encontrar último bloco da cadeia liberada
        cur = start
        prev = None
        while cur != NULL_PTR:
            prev = cur
            cur = self.ptr[cur]
        if prev is not None:
            self.ptr[prev] = self.free_head
            self.free_head = start
            self.free_count += count
        print(f"[OK] Arquivo '{name}' removido. {count} bloco(s) liberado(s).")
        return True
    
    # imprime disco com detalhes (índice, dado como char ou '.', ponteiro)
    def print_disk(self):
        print("DISCO (índice : dado (ord) -> ponteiro):")
        for i in range(NUM_BLOCKS):
            data_val = self.data[i]
            ch = '.' if data_val == 0 else (chr(data_val) if 32 <= data_val <= 126 or data_val >= 160 else chr(data_val))
            ptr = self.ptr[i]
            ptr_str = 'NULL' if ptr == NULL_PTR else str(ptr)
            print(f" {i:02d}: '{ch}' ({data_val}) -> {ptr_str}")
        print(f"Free head: {self.free_head}  | Free count: {self.free_count}")
    
    # imprime tabela de diretório
    def print_directory(self):
        print("TABELA DE DIRETÓRIO (nome -> bloco inicial):")
        if not self.directory:
            print(" <vazia>")
        for name, start in self.directory.items():
            start_str = 'NULL' if start == NULL_PTR else str(start)
            print(f"  {name} -> {start_str}")
    
    # imprime índices de blocos livres (seguindo a lista encadeada)
    def print_free_indices(self, limit=200):
        seq = []
        cur = self.free_head
        cnt = 0
        while cur != NULL_PTR and cnt < limit:
            seq.append(cur)
            cur = self.ptr[cur]
            cnt += 1
        print(f"Índices livres (até {limit}): {seq}")
        print(f"Total livres (contagem mantida): {self.free_count}")
    
    # imprime conteúdo do arquivo (mesma função read_file, mas formatada)
    def print_file(self, name):
        content = self.read_file(name)
        # read_file já imprime
    
# Demonstração conforme exemplo do enunciado
def demo():
    fs = FileSystem()
    print("=== INÍCIO DO DISCO (vazio) ===")
    fs.print_directory()
    fs.print_free_indices()
    print()
    
    # Inserir arquivos (exemplo): f1, f2, f3
    # Conteúdos ilustrativos (cada caractere ocupa 1 bloco)
    print(">>> Inserindo f1 = 'BR' (exemplo pequeno)")
    fs.create_file('f1', 'BR')   # dois blocos
    print(">>> Inserindo f2 = 'São Paulo'")
    fs.create_file('f2', 'São Paulo')  # vários blocos (inclui espaço e caractere especial)
    print(">>> Inserindo f3 = 'Minas Gerais'")
    fs.create_file('f3', 'Minas Gerais')
    print()
    fs.print_directory()
    fs.print_free_indices()
    print()
    
    # Tentar inserir f4 = "Santa Catarina" que deve estourar espaço em exemplo do enunciado
    content_f4 = "Santa Catarina"
    print(f">>> Tentativa de inserir f4 = '{content_f4}' (deve falhar se espaço insuficiente)")
    ok = fs.create_file('f4', content_f4)
    if not ok:
        print("-> Inserção falhou como esperado (memória insuficiente).")
    print()
    
    # Mostrar disco detalhado
    # fs.print_disk()
    
    # Remover f2
    print(">>> Removendo f2 ('São Paulo')")
    fs.delete_file('f2')
    fs.print_directory()
    fs.print_free_indices()
    print()
    
    # Tentar inserir f4 novamente
    print(f">>> Tentativa de inserir f4 = '{content_f4}' novamente (deve ter sucesso se espaço foi liberado)")
    ok2 = fs.create_file('f4', content_f4)
    if ok2:
        print("-> Inserção bem-sucedida.")
    print()
    fs.print_directory()
    fs.print_free_indices()
    print()
    
    # Ler os arquivos existentes
    print(">>> Leitura de arquivos presentes:")
    for nome in list(fs.directory.keys()):
        fs.print_file(nome)
    print()
    print("=== FIM DA DEMONSTRAÇÃO ===")
    return fs

if __name__ == "__main__":
    demo()
