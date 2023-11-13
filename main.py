import json
import time
from datetime import datetime

# Constantes
ARQUIVO_VIAS = 'vias.json'
ARQUIVO_RELATORIOS = 'relatorios.json'
CORES_SEMAFORO_VALIDAS = ['vermelho', 'verde']


# Funções auxiliares para interação com arquivos JSON
def carregar_dados_arquivo(nome_arquivo):
    """Carrega dados de um arquivo JSON e trata exceções relacionadas ao arquivo."""
    try:
        with open(nome_arquivo, 'r') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao carregar o arquivo {nome_arquivo}: {e}")
        return {}


def salvar_dados_arquivo(nome_arquivo, dados):
    """Salva dados em um arquivo JSON e trata exceções de IO."""
    try:
        with open(nome_arquivo, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)
        return True
    except IOError as e:
        print(f"Erro ao escrever no arquivo {nome_arquivo}: {e}")
        return False


# Funções para validação de data e horário
def validar_data(data):
    """Valida se uma string de data está no formato dd/mm/aaaa."""
    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False


def validar_horario(horario):
    """Valida se uma string de horário está no formato hh:mm."""
    try:
        datetime.strptime(horario, '%H:%M').time()
        return True
    except ValueError:
        return False


# Função para monitoramento das vias
def monitorar_vias(vias):
    """Exibe o status atual das vias e seus semáforos."""
    print('\nMonitoramento das vias:')
    for via, info in vias.items():
        print(f"{via}: {info['status']} - Semáforo: {info['semaforo']}")
    time.sleep(5)


# Função para criação de relatório
def fazer_relatorio(vias, relatorios):
    """Permite ao usuário criar um novo relatório para uma via específica."""
    print("\nVias disponíveis:")
    for idx, via in enumerate(vias, start=1):
        print(f"{idx}. {via}")

    escolha_valida = False
    while not escolha_valida:
        try:
            escolha = int(input("\nEscolha o número da via para o relatório: "))
            if 1 <= escolha <= len(vias):
                nome_via = list(vias.keys())[escolha - 1]
                escolha_valida = True
            else:
                print("Número inválido! Tente novamente.")
        except ValueError:
            print("Digite um número válido!")

    horario = input("Horário do acontecimento (hh:mm): ")
    while not validar_horario(horario):
        print("Horário no formato inválido! Tente novamente.")
        horario = input("Horário do acontecimento (hh:mm): ")

    dia = input("Dia do relatório (dd/mm/aaaa): ")
    while not validar_data(dia):
        print("Data no formato inválido! Tente novamente.")
        dia = input("Dia do relatório (dd/mm/aaaa): ")

    acontecimento = input("Qual o acontecimento? ")
    relatorio = {
        "nome_via": nome_via,
        "horario": horario,
        "acontecimento": acontecimento,
        "dia": dia
    }
    relatorios.append(relatorio)
    print("\nRelatório adicionado com sucesso!")
    salvar_dados_arquivo(ARQUIVO_RELATORIOS, relatorios)


# Função para visualização dos relatórios
def ver_relatorios(relatorios):
    """Exibe todos os relatórios criados."""
    print('\nRelatórios:')
    for rel in relatorios:
        print(f'Via: {rel["nome_via"]}\nHorário: {rel["horario"]}\nAcontecimento: {rel["acontecimento"]}\nDia: {rel["dia"]}\n')
    time.sleep(5)


# Função de busca de relatórios
def buscar_relatorios(relatorios, criterio):
    """Busca relatórios por um critério específico de nome da via ou data."""
    return [rel for rel in relatorios if criterio.lower() in rel['nome_via'].lower() or criterio in rel['dia']]


# Adição da função de busca de relatórios no menu
def menu_buscar_relatorios(relatorios):
    criterio = input("Digite o nome da via ou data (dd/mm/aaaa) para buscar relatórios: ")
    relatorios_encontrados = buscar_relatorios(relatorios, criterio)
    if relatorios_encontrados:
        print("\nRelatórios encontrados:")
        for rel in relatorios_encontrados:
            print(f'Via: {rel["nome_via"]}\nHorário: {rel["horario"]}\nAcontecimento: {rel["acontecimento"]}\nDia: {rel["dia"]}\n')
    else:
        print("Nenhum relatório correspondente ao critério encontrado.")
    time.sleep(5)


def mudar_semaforos(vias):
    """Permite ao usuário mudar a cor de um semáforo para uma via específica."""
    print('\nMudar semáforo:')
    for idx, via in enumerate(vias.keys(), 1):
        print(f'{idx}. {via}')

    escolha = input('\nEscolha uma via pelo número ou nome: ').strip()
    if escolha.isdigit():
        escolha = int(escolha) - 1
        via_selecionada = list(vias.keys())[escolha] if 0 <= escolha < len(vias) else None
    else:
        via_selecionada = escolha if escolha in vias else None

    if via_selecionada is None:
        print('Via selecionada é inválida!')
        return

    cor = input('Escolha uma cor para o semáforo (vermelho/verde): ').lower()
    if cor not in CORES_SEMAFORO_VALIDAS:
        print('Cor inválida! Por favor, escolha uma cor válida: vermelho ou verde.')
        return

    vias[via_selecionada]['semaforo'] = cor
    if salvar_dados_arquivo(ARQUIVO_VIAS, vias):
        print(f'\nSemáforo da {via_selecionada} mudado para {cor} com sucesso!')

# Carregamento inicial de dados
vias = carregar_dados_arquivo(ARQUIVO_VIAS)
relatorios = carregar_dados_arquivo(ARQUIVO_RELATORIOS)
if not isinstance(relatorios, list):  # Garante que relatorios seja uma lista
    relatorios = []

# Loop principal do menu
while True:
    print('\n----------------------------------')
    print('| SISTEMA DE CONTROLE DE TRÁFEGO |')
    print('----------------------------------')
    print('[1] - Monitoramento da via')
    print('[2] - Fazer relatórios')
    print('[3] - Ver relatórios')
    print('[4] - Buscar relatórios')
    print('[5] - Mudar semáforos')
    print('[6] - Encerrar o programa')

    opcao = input('\nDigite a opção desejada: ')
    if not opcao.isdigit() or not 1 <= int(opcao) <= 6:
        print('\nPor favor, digite um número válido!')
        continue
    opcao = int(opcao)

    match opcao:
        case 1:
            monitorar_vias(vias)
        case 2:
            fazer_relatorio(vias, relatorios)
        case 3:
            ver_relatorios(relatorios)
        case 4:
            menu_buscar_relatorios(relatorios)
        case 5:
            mudar_semaforos(vias)
        case 6:
            print('Encerrando programa...')
            if salvar_dados_arquivo(ARQUIVO_VIAS, vias) and salvar_dados_arquivo(ARQUIVO_RELATORIOS, relatorios):
                print('Dados salvos com sucesso.')
            else:
                print('Houve um problema ao salvar alguns dados.')
            time.sleep(1)
            break
