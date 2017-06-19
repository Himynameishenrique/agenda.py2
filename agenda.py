import sys, time # time pra amanha e hoje

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração.

def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '':
    return False 
  extralist = []
  data = ''
  hora = ''
  pri = ''
  contexto = ''
  projeto = ''
  novaAtividade = ''
  if extras == '':
    novaAtividade = descricao
  else:
    extralist.append(extras[0])
    extralist.append(extras[1])
    extralist.append(extras[2])
    extralist.append(descricao)
    extralist.append(extras[3])
    extralist.append(extras[4])
    for x in extralist:
      if len(x) > 0:
        novaAtividade = novaAtividade + x + ' '
    novaAtividade = novaAtividade.strip()
  # Escreve no TODO_FILE. 
  try: 
    fp = open('todo.txt', 'a', encoding = 'latin1') # encoding alterado pois estava dando problemas em acentos
    if fp == None:
      print ("Erro ao abrir o arquivo\n")
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + todo.txt)
    print(err)
    return False

  return True

# transforma de lista organizada pra lista de strings como estaria no todo.txt ou done.txt
def desorganizar(listaOriginal):
  aux = []
  listaCompleta = listaOriginal[:]
  while listaCompleta:
    extralist = []
    data = ''
    hora = ''
    pri = ''
    contexto = ''
    projeto = ''
    novaAtividade = ''
    lista = listaCompleta.pop(0)
    if lista[1] == '':
      novaAtividade = lista[0]
    else:
      extralist.append(lista[1][0])
      extralist.append(lista[1][1])
      extralist.append(lista[1][2])
      extralist.append(lista[0])
      extralist.append(lista[1][3])
      extralist.append(lista[1][4])
      for x in extralist:
        if len(x) > 0:
          novaAtividade = novaAtividade + x + ' '
      novaAtividade = novaAtividade.strip()
      aux.append(novaAtividade)
  return aux

# faz o mesmo que acima, porém sabe que tem uma numeração nas futuras linhas agora
def desorganizarNumerado(listaOriginal):
  aux = []
  listaCompleta = listaOriginal[:]
  while listaCompleta:
    extralist = []
    data = ''
    hora = ''
    pri = ''
    contexto = ''
    projeto = ''
    novaAtividade = ''
    lista = listaCompleta.pop(0)
    if lista[1] == '':
      novaAtividade = lista[1]
    else:
      extralist.append(lista[0])
      extralist.append(lista[2][0])
      extralist.append(lista[2][1])
      extralist.append(lista[2][2])
      extralist.append(lista[1])
      extralist.append(lista[2][3])
      extralist.append(lista[2][4])
      for x in extralist:
        if len(x) > 0:
          novaAtividade = novaAtividade + x + ' '
      novaAtividade = novaAtividade.strip()
      aux.append(novaAtividade)
  return aux

# Valida a prioridade.-------------------------------------------------------OK
def prioridadeValida(pri):
  if pri[0] != '(' or pri[2] != ')' or len(pri) != 3:
    return False
  return True


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA. ---------------------------OK
def horaValida(horaMin):
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  if int(horaMin[0] + horaMin[1]) > 23 or int(horaMin[0] + horaMin[1]) < 0:
    return False
  if int(horaMin[2]) > 5:
    return False
  return True

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto.----------------------------------------OK
def dataValida(data):
  if len(data) != 8 or not soDigitos(data):
    return False
  dia = int(data[0:2])
  mes = int(data[2:4])
  ano = int(data[4:8])
  if dia > 31: # Teste rapido do dia válido
    return False
  elif mes > 12 or mes < 1: #Teste do mês valido
    return False
  elif ano < 2017: #Teste para ver se o ano já passou
    return False
  else:
    if mes == 2: #Teste de Fevereiro
      if dia > 29:
        return False
      
        #Teste de Abril, Junho, Setembro, Novembro
    elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
      if dia > 30:
        return False
  return True

# Valida que o string do projeto está no formato correto.--------------OK
def projetoValido(proj):
  if len(proj) < 2 or proj[0] != '+':
    return False
  return True
  
# Valida que o string do contexto está no formato correto.-------------OK
def contextoValido(cont):
  if len(cont) < 2 or cont[0] != '@':
    return False
  return True

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim. -----------------------------------------OK
def soDigitos(numero):
  if type(numero) != str:
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.-----------------------------------------OK

def organizar(linhas):
  itens = []
  aux=[]
  
    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

  while linhas:
    desc = ''
    data = ''
    hora = ''
    pri = ''
    contexto = ''
    projeto = ''
    aux = linhas.pop(0)
    aux = aux.strip()
    aux = aux.split(' ')
    if dataValida(aux[0]) and len(data)== 0: #Checa se as variáveis também já não foram preenchidas em outra situação
      data=aux.pop(0)
    if horaValida(aux[0]) and len(hora)== 0:
      hora=aux.pop(0)
    if prioridadeValida(aux[0]) and len(pri)== 0:
      pri=aux.pop(0)
      
    # agora temos a descrição
    if len(aux) > 1: # descricao e mais algo pelo menos
      if projetoValido(aux[len(aux)-1]) and len(projeto)== 0:
        projeto=aux.pop(len(aux)-1)
    if len(aux) > 1: # necessário checar pois o pop pode ter tirado o último elemento que não era descrição
      if contextoValido(aux[len(aux)-1]) and len(contexto)== 0:
        contexto=aux.pop(len(aux)-1)
    desc = ' '.join(aux)
    itens.append((desc, (data, hora, pri, contexto, projeto)))
    
  return itens

# Adiciona o número da linha nas tuplas, só coloca uma tupla se ela respeita
# as restrições opcionais do commando l, se existirem
def numeraLista(listaDeTuplas, lData = '', lPri='', lCont ='', lProj=''):
  listaFormatada = []
  for i in range(len(listaDeTuplas)):
    okData = True
    okPri = True
    okCont = True
    okProj = True
    novaData = formataData(listaDeTuplas[i][1][0])
    novaHora = formataHora(listaDeTuplas[i][1][1])
    if lData or lPri or lCont or lProj:
      if lData and lData != listaDeTuplas[i][1][0]:
        okData = False
      if lPri and lPri != listaDeTuplas[i][1][2]:
        okPri = False
      if lCont and lCont != listaDeTuplas[i][1][3].lower(): #lower pra ficar mais leniente. Apenas na comparação, guarda como o usuário digitou originalmente
        okCont = False
      if lProj and lProj != listaDeTuplas[i][1][4].lower():
        okProj = False

      if okData and okPri and okCont and okProj:
        listaFormatada.append((str(i + 1), listaDeTuplas[i][0], (novaData, novaHora, listaDeTuplas[i][1][2], listaDeTuplas[i][1][3], listaDeTuplas[i][1][4])))

    else:
      listaFormatada.append((str(i + 1), listaDeTuplas[i][0], (novaData, novaHora, listaDeTuplas[i][1][2], listaDeTuplas[i][1][3], listaDeTuplas[i][1][4])))
  return listaFormatada

# recebe data no formato ddmmaaaa e retorna no formato dd/mm/aaaa
def formataData(data):
  if data:
    dia = data[0:2]
    mes = data[2:4]
    ano = data[4:8]
    return dia + '/' + mes + '/' + ano
  else:
    return ''

# recebe hora no formato HHMM e retorna no formato HH:MM
def formataHora(HHMM):
  if HHMM:
    hora = HHMM[0:2]
    minuto = HHMM[2:4]
    return hora + ':' + minuto
  else:
    return ''
  
# retorna -1 se data1 < data2, 1 se data1 > data2, 0 se data1 == data2
def dataComp(data1, data2):
  if data1 and not data2:
    return -1
  if data2 and not data1:
    return 1
  if not data2 and not data1:
    return 0
  
  dia1 = int(data1[0:2])
  mes1 = int(data1[3:5])
  ano1 = int(data1[6:10])
  
  dia2 = int(data2[0:2])
  mes2 = int(data2[3:5])
  ano2 = int(data2[6:10])
  if ano1 < ano2:
    return -1
  if ano1 > ano2:
    return 1
  # anos iguais
  if mes1 < mes2:
    return -1
  if mes1 > mes2:
    return 1
  # meses iguais
  if dia1 < dia2:
    return -1
  if dia1 > dia2:
    return 1
  # tudo igual
  return 0

# retorna -1 ser HHMM1 < HHMM2, 1 se HHMM1 > HHMM2, 0 se HHMM1 == HHMM2
def horaComp(HHMM1, HHMM2):
  if HHMM1 and not HHMM2:
    return -1
  if HHMM2 and not HHMM1:
    return 1
  if not HHMM2 and not HHMM1:
    return 0
  
  hora1 = int(HHMM1[0:2])
  minuto1 = int(HHMM1[3:5])

  hora2 = int(HHMM2[0:2])
  minuto2 = int(HHMM2[3:5])

  if hora1 < hora2:
    return -1
  if hora1 > hora2:
    return 1
  
  # horas iguais

  if minuto1 < minuto2:
    return -1
  if minuto1 > minuto2:
    return 1

  # tudo igual
  return 0

# pega uma data e retorna o dia seguinte
# fevereiro sempre pode ter 29 dias, não se preocupa com bissexto.
def amanha(data):
  dia = int(data[0:2])
  mes = int(data[2:4])
  ano = int(data[4:8])

  if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
    if dia == 31:
      dia = 1
      if mes == 12:
        mes = 1
        ano = ano + 1
      else:
        mes = mes + 1
    else:
      dia = dia + 1

  if mes == 2:
    if dia == 29:
      dia = 1
      mes = 3
    else:
      dia = dia + 1
  else:
    if dia == 30:
      dia = 1
      mes = mes + 1
    else:
      dia = dia + 1

  dia = str(dia)
  mes = str(mes)
  ano = str(ano)
  if len(dia) < 2:
    dia = '0' + dia
  if len(mes) < 2:
    mes = '0' + mes
  while len(ano) < 4:
    ano = '0' + ano
  
  return str(dia) + str(mes) + str(ano)

#bubble sort cuja chave de comparação é a prioridade!
def bubbleSortPrioridade(listaDeTuplas):
  ok = len(listaDeTuplas)
  # ok nos diz quantos itens ainda não estão na posição correta.
  # como o bubble sort arruma no mínimo 1 item por iteração, basta
  # iterar no mínimo len(listaDeTuplas) vezes que todos os elementos estarão ordenados no fim
  for i in range(len(listaDeTuplas)):
    for j in range(1, ok):
      chave1 = listaDeTuplas[j-1][2][2]
      chave2 = listaDeTuplas[j][2][2]
      if (chave1 > chave2 and chave2) or (chave2 and not chave1): # se chave1 nao existir e chave2 existir, então chave2 deve subir
        listaDeTuplas[j-1], listaDeTuplas[j] = listaDeTuplas[j], listaDeTuplas[j-1]
    ok = ok - 1

# bubble sort cuja chave primária de comparação é a data, secundária é a hora!
def bubbleSortDataHora(listaDeTuplas):
  ok = len(listaDeTuplas) 
  for i in range(len(listaDeTuplas)):
    for j in range(1, ok):
      p1 = listaDeTuplas[j-1][2][2]
      p2 = listaDeTuplas[j][2][2]
      
      data1 = listaDeTuplas[j-1][2][0]
      data2 = listaDeTuplas[j][2][0]
      
      hora1 = listaDeTuplas[j-1][2][1]
      hora2 = listaDeTuplas[j][2][1]
      # se prioridade existir, não tocar
      if ((dataComp(data1, data2) == 1 and data2) or (not data1 and data2)) and (p1 == p2 or not (p1 or p2)):
        listaDeTuplas[j-1], listaDeTuplas[j] = listaDeTuplas[j], listaDeTuplas[j-1]
      # se as datas forem iguais, o desempate pode ser na hora, a chave secundária.
      elif data1 == data2 and ((horaComp(hora1, hora2) == 1 and hora2) or (not hora1 and hora2)) and (p1 == p2 or not (p1 or p2)):
        listaDeTuplas[j-1], listaDeTuplas[j] = listaDeTuplas[j], listaDeTuplas[j-1]
    ok = ok - 1

# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar(criterios=[]):
  tuplaOrganizada=[]
  arq=open('todo.txt','r+', encoding='latin1') # estava dando problema com acentos, por isso latin1
  linhas=arq.read() # lê todas as linhas do arquivo, retorna um string só
  linhas = linhas.splitlines() # cria uma lista onde cada elemento é uma linha do arquivo texto
  tuplaOrganizada = organizar(linhas) # organiza cada linha e devolve
  if criterios:
    data = ''
    pri = ''
    cont = ''
    proj = ''
    while criterios: # se existirem criterios, ir validando eles e descartando os inválidos
      if dataValida(criterios[0][0:2] + criterios[0][3:5] + criterios[0][6:10]):
        data = criterios[0][0:2] + criterios[0][3:5] + criterios[0][6:10]
        criterios.pop(0)
      elif criterios[0].lower() == 'hoje':
        criterios.pop(0)
        data = time.strftime("%d%m%Y") # pega hoje e passa hoje, eventualmente
      elif criterios[0].lower() == 'amanhã' or criterios[0].lower() == 'amanha':
        criterios.pop(0)
        data = amanha(time.strftime("%d%m%Y")) # pega hoje e transforma em amanhã
      elif prioridadeValida('(' + criterios[0].upper() + ')'):
        pri = '(' + criterios.pop(0).upper() + ')'
      elif contextoValido(criterios[0].lower()):
        cont = criterios.pop(0).lower()
      elif projetoValido(criterios[0].lower()):
        proj = criterios.pop(0).lower()
      else:
        criterios.pop(0) # descartar se for inválido
    # quando tiver feito isso com todos os criterios, os dá para numeraLista, que vai retornar apenas
    # as tuplas que respeitam as restrições
    tuplaOrganizada = numeraLista(tuplaOrganizada, lData=data, lPri=pri, lCont=cont, lProj = proj)
  else: # senão, pega todas as tuplas
    tuplaOrganizada = numeraLista(tuplaOrganizada)
  ordenarPorPrioridade(tuplaOrganizada)
  ordenarPorDataHora(tuplaOrganizada)
  agendaOrganizada = desorganizarNumerado(tuplaOrganizada) # transforma a lista de tuplas em lista de strings como estaria no arquivo texto

  # imprime com as formatações
  for n, x in enumerate(agendaOrganizada): #enumerate nos dá o índice, para podermos checar facilmente na tuplaOrganizada por prioridade
    if tuplaOrganizada[n][2][2] == '(A)':
      printCores(x, RED) #+ BOLD) não está funcionando
    elif tuplaOrganizada[n][2][2] == '(B)':
      printCores(x, BLUE)
    elif tuplaOrganizada[n][2][2] == '(C)':
      printCores(x, CYAN)
    elif tuplaOrganizada[n][2][2] == '(D)':
      printCores(x, GREEN)
    else:
      print(x)
  return

def ordenarPorDataHora(itens):
  bubbleSortDataHora(itens)
  return itens
   
def ordenarPorPrioridade(itens):
  bubbleSortPrioridade(itens)
  return itens

def fazer(num):
  arq = open('todo.txt', 'r', encoding = 'latin1')
  linhas = arq.read()
  arq.close()
  linhas = linhas.splitlines() # pega as linhas
  try:
    linhas[num] # checa se existe a que pediu
  except IndexError:
    print('Esta atividade não existe:', num + 1)
    return
  
  arq = open('todo.txt', 'w', encoding = 'latin1')
  for n, x in enumerate(linhas):
    if n != num: # exclui a que pediu pra colocar em done.txt
      arq.write(x + '\n')
  arq.close()
  arqdone = open('done.txt', 'a', encoding = 'latin1')
  arqdone.write(linhas[num] + '\n') # coloca ela em done.txt
  arqdone.close()
  return 

def remover(num):
  arq = open('todo.txt', 'r', encoding = 'latin1')
  linhas = arq.read()
  arq.close()
  linhas = linhas.splitlines()
  try:
    linhas[num] # checa se existe a linha num
  except IndexError:
    print('Esta atividade não existe:', num + 1)
    return
  
  arq = open('todo.txt', 'w', encoding = 'latin1')
  for n, x in enumerate(linhas):
    if n != num: # exclui a linha num
      arq.write(x + '\n')
  arq.close()
  return

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
  arq = open('todo.txt', 'r', encoding = 'latin1')
  linhas = arq.read()
  arq.close()
  linhas = linhas.splitlines()
  
  try:
    atualizar = linhas[num]
  except IndexError:
    print('Esta atividade não existe:', num + 1)
    return

  # para alterar a prioridade, organizamos ela pra ficar no formato onde sabemos exatamente onde cada coisa está
  manejavel = organizar([atualizar])[0]
  # criamos uma nova tupla atualizando a prioridade
  atualizado = (manejavel[0], (manejavel[1][0], manejavel[1][1], '(' + prioridade + ')', manejavel[1][3], manejavel[1][4]))
  # devolvemos a tupla pro formato que fica no todo.txt
  atualizado = desorganizar([atualizado])[0]
  arq = open('todo.txt', 'w', encoding = 'latin1')
  for n, x in enumerate(linhas):
    if n == num: # atualiza a alterada
      arq.write(atualizado + '\n')
    else: # o resto igual
      arq.write(x + '\n')
  arq.close()
  return

# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if len(comandos) < 2:
    print("Preciso de mais argumentos!")
    return
  
  comandos.pop(0) # remove 'agenda.py'
  if comandos[0] == ADICIONAR:
    comandos.pop(0) # remove 'adicionar'
    if len(comandos) == 0:
      print("Preciso de mais argumentos!")
      return
    try:
      itemParaAdicionar = organizar([' '.join(comandos)])[0]
    except IndexError:
      print('Formato inválido!')
      return
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
    
  elif comandos[0] == LISTAR:
    comandos.pop(0) # remove 'listar'
    if len(comandos) > 0:
      listar(comandos)
    else:
      listar()
    return    

  elif comandos[0] == REMOVER:
    comandos.pop(0) # remove 'remover'
    if len(comandos) == 0:
      print("Preciso de mais argumentos!")
      return
    remover(int(comandos[0]) - 1) # - 1 pois listar mostra o primeiro como 1
    return
  
  elif comandos[0] == FAZER:
    comandos.pop(0) # remove 'fazer'
    if len(comandos) == 0:
      print("Preciso de mais argumentos!")
      return
    fazer(int(comandos[0]) - 1) # -1 pois listar mostra o primeiro como 1
    return
  
  elif comandos[0] == PRIORIZAR:
    comandos.pop(0) # remove 'priorizar'
    if len(comandos) < 2:
      print("Preciso de mais argumentos!")
      return
    priorizar(int(comandos[0]) - 1, comandos[1].upper()) # - 1 pois listar mostra o primeiro como 1, upper pra caso esteja minúsculo
    return
  
  else:
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']

processarComandos(sys.argv)
