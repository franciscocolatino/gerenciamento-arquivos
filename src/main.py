import file_system
    
# Demonstração conforme exemplo do enunciado
def example():
    fs = file_system.FileSystem()
    print("--- INÍCIO DO DISCO (vazio) ---")
    fs.print_directory()
    fs.print_free_indices()
    print()
    
    # Inserir arquivos (exemplo): f1, f2, f3
    # Conteúdos ilustrativos (cada caractere ocupa 1 bloco)
    print("Inserindo f1 = 'BR' (exemplo pequeno)")
    fs.create_file('f1', 'BR')   # dois blocos
    print("Inserindo f2 = 'São Paulo'")
    fs.create_file('f2', 'São Paulo')  # vários blocos (inclui espaço e caractere especial)
    print("Inserindo f3 = 'Minas Gerais'")
    fs.create_file('f3', 'Minas Gerais')
    print()
    fs.print_directory()
    fs.print_free_indices()
    print()
    
    # Tentar inserir f4 = "Santa Catarina" que deve estourar espaço em exemplo do enunciado
    content_f4 = "Santa Catarina"
    print(f"Tentativa de inserir f4 = '{content_f4}' (deve falhar se espaço insuficiente)")
    ok = fs.create_file('f4', content_f4)
    if not ok:
        print("-> Inserção falhou como esperado (memória insuficiente).")
    print()
    
    # Mostrar disco detalhado
    fs.print_disk()
    
    # Remover f2
    print("Removendo f2 ('São Paulo')")
    fs.delete_file('f2')
    fs.print_directory()
    fs.print_free_indices()
    print()
    
    # Tentar inserir f4 novamente
    print(f"Tentativa de inserir f4 = '{content_f4}' novamente (deve ter sucesso se espaço foi liberado)")
    ok2 = fs.create_file('f4', content_f4)
    if ok2:
        print("Inserção bem-sucedida.")
    print()
    fs.print_directory()
    fs.print_free_indices()
    print()
    
    fs.print_disk()
    
    # Ler os arquivos existentes
    print("Leitura de arquivos presentes:")
    for nome in list(fs.directory.keys()):
        fs.print_file(nome)
    print()
    print("--- FIM DA DEMONSTRAÇÃO ---")
    return fs

if __name__ == "__main__":
    example()
