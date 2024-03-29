#############
#
# ImperadorTelemetria.py
# Escrito para rodar no Windows 11
#
#
# Autor: Rafael Eijy Ishikawa Rasoto - Lambari
#
###########

import tkinter #tk
from tkinter import ttk
import os
from PIL import Image, ImageTk # Pillow
import serial.tools.list_ports # pyserial
import continuous_threading # continuous_threading
import datetime
import numpy  #numpy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation #matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from drawnow import * #drawnow
import pandas as pd #pandas
import re






###### Variáveis

portaCOM = 'COM3'

serialInst = serial.Serial()

ports = serial.tools.list_ports.comports()
portList = []

for onePort in ports:
    portList.append(str(onePort))

statusConexao = False
baudrate = 9600


velocidadeAtual = 0
rpmAtual = 0
freioAtual  = False
temperaturaAtual = 0
bateriaAtual = 0
aceleracaoX = 0
aceleracaoY = 0
aceleracaoZ = 0
anguloX = 0
anguloY = 0
anguloZ = 0
velocidadeGPS = 0

box_estado = False
box_enviar = False


dataVel = []
dataRPM = []
dataBateria = []
dataTemperatura = []
dataFreio = []
dataTempo = []
dataVelGPS = []

dataAccX = []
dataAccY = []
dataAccZ = []
dataAngX = []
dataAngY = []
dataAngZ = []


fGrafico = Figure(figsize=(14, 7), dpi=100)
grafVel = fGrafico.add_subplot(221)
grafRPM = fGrafico.add_subplot(222)
grafTemp = fGrafico.add_subplot(223)
grafBat = fGrafico.add_subplot(224)


###### Eventos

def eventoSelectBaudRate(baudRate_recebido):
   
    baudRate_recebido = varBaudRate.get()
    print("Baud Rate recebido: " + baudRate_recebido)

    global baudrate
    baudrate = baudRate_recebido
    print("Variável BaudRate: " + str(baudrate))

    return
    


def eventoSelectCOM(COM_recebido):

    global portaCOM

    COM_recebido = varPortaCOM.get()

    COM_recebido = COM_recebido[0:4]

    print(COM_recebido)

    
    for i in range(0, len(portList)):

        if COM_recebido in  portList[i]:
            portaCOM = portList[i][0:4]

    return


def eventoBotaoConectar():
    global statusConexao
    global serialInst
    
    if statusConexao == False:
        
        statusConexao = True
        conectarBotao.configure(text="Desconectar")
        statusConexaoLabel.configure(text="Conectado", bg="green")
        serialInst.baudrate = baudrate
        serialInst.port = portaCOM
        serialInst.open()
        serialInst.flush()
        return
    
    statusConexao = False
    conectarBotao.configure(text="Conectar")
    statusConexaoLabel.configure(text="Desconectado", bg = "red")
    serialInst.close()

    return

def eventoBotaoApagar():
    textoRecebido.delete("0.0", "end")
    return

def eventoBotaoEnviar():
    print("Enviar")
    return


def eventoBotaoBox():

    global box_enviar
    box_enviar = True

    return


def eventoExportarExcel():
    
    data = {
        'horario': dataTempo,
        'velocidade': dataVel,
        'RPM': dataRPM,
        'Temperatura': dataTemperatura,
        'Bateria': dataBateria,
        'Freio': dataFreio,
        'AccX': aceleracaoX,
        'AccY': aceleracaoY,
        'AccZ': aceleracaoZ,
        'AngX': anguloX,
        'AngY': anguloY,
        'AngZ': anguloZ,
        'velocidadeGPS': dataVelGPS
    }

    df = pd.DataFrame(data)

    df.to_excel(r'C:\Users\rafae\OneDrive\Documentos\Code\Baja\BajaImperador\2023-2\Telemetria\planilha\data.xlsx', index=False)

    return


###### JANELA PRINCIPAL

janela = tkinter.Tk()
janela.geometry("1920x950")
janela.title("Imperador - Telemetria")
janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(1, weight=1)





###### FONTES

fonteTitulo = ("Impact", 20, "bold")
fonteBotao = ("Oswald", 20)
fonteTexto = ("Oswald", 12)





###### IMAGENS 

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")

imagemLogo          = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "Logo.png")).resize((200,100), Image.Resampling.LANCZOS))
imagemConexao       = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "Conexao.png")).resize((50,50), Image.Resampling.LANCZOS))
imagemTelemetria    = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "Telemetria.png")).resize((50,50), Image.Resampling.LANCZOS))
imagemLog           = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "Log.png")).resize((50,50), Image.Resampling.LANCZOS))
imagemBorracha      = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "Borracha.png")).resize((30,30), Image.Resampling.LANCZOS))
imagemFreio         = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "Freio.png")).resize((50,50), Image.Resampling.LANCZOS))
imagemTemperatura   = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "Temperatura.png")).resize((50,50), Image.Resampling.LANCZOS))
imagemBateria       = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "Bateria.png")).resize((50,50), Image.Resampling.LANCZOS))
imagemVelocidade    = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "Velocidade.png")).resize((50,50), Image.Resampling.LANCZOS))
imagemRpm           = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "Rpm.png")).resize((50,50), Image.Resampling.LANCZOS))
imagemConectar      = ImageTk.PhotoImage(Image.open(os.path.join(image_path, "Conectar.png")).resize((25,25), Image.Resampling.LANCZOS))






###### TELAS DO SISTEMA

frameConexao = tkinter.Frame(janela)
frameConexao.grid_columnconfigure(0, weight=1)
frameConexao.grid(row=0, column=1, sticky="nsew")

frameTelemetria = tkinter.Frame(janela)
frameTelemetria.grid_rowconfigure(1, weight=1)

frameLog = tkinter.Frame(janela)
frameLog.grid_columnconfigure(0, weight=1)

frameNavegacao = tkinter.Frame(janela)
frameNavegacao.grid(row=0, column=0, sticky="nsew")
frameNavegacao.grid_rowconfigure(5, weight=1)





###### Frame de Conexão

statusConexaoLabel = tkinter.Label(frameConexao, bg="red" if statusConexao == False else "green", text="Desconectado" if statusConexao == False else "Conectado", font=fonteBotao)
statusConexaoLabel.grid(row=0, column=0, padx=20, pady=20)

baudRateLabel = tkinter.Label(frameConexao, text="Baud-Rate", font=fonteBotao)
baudRateLabel.grid(row=1, column=0, padx=20, pady=10)


listaBaudRate = ["9600", "38400", "115200"]
varBaudRate = tkinter.StringVar(frameConexao)
varBaudRate.set(listaBaudRate[0])

baudRateSelector = tkinter.OptionMenu(frameConexao, varBaudRate, *listaBaudRate, command=eventoSelectBaudRate)
baudRateSelector.grid(row = 2, column=0, padx=20, pady=10)

portaCOMLabel = tkinter.Label(frameConexao, text="Porta COM", font=fonteBotao)
portaCOMLabel.grid(row=3, column=0, padx=20, pady=0)

varPortaCOM = tkinter.StringVar()
varPortaCOM.set("COM3")

portaCOMSelector = tkinter.OptionMenu(frameConexao, varPortaCOM, *portList, command=eventoSelectCOM)
portaCOMSelector.grid(row=4, column=0, padx=20, pady=10)

conectarBotao = tkinter.Button(frameConexao, text="Conectar" if statusConexao == False else "Desconectar", image = imagemConectar, command=eventoBotaoConectar)
conectarBotao.grid(row=5, column=0, padx=20, pady=10)

textoRecebido = tkinter.Text(frameConexao, state="normal", font=fonteTexto, width=50, height=10)
textoRecebido.grid(row=6, column=0, padx=20, pady=10)

apagarBotao = tkinter.Button(frameConexao, text="Apagar", image=imagemBorracha, command=eventoBotaoApagar)
apagarBotao.grid(row=7, column=0, padx=20, pady=0)

textoComando = tkinter.Text(frameConexao, state = "disabled" if statusConexao == False else "normal", font=fonteTexto, width=50, height=1)
textoComando.grid(row=8, column=0, padx=20, pady=10)

enviarBotao = tkinter.Button(frameConexao, text="Enviar", state= "disabled" if statusConexao == False else "normal", command=eventoBotaoEnviar)
enviarBotao.grid(row=9, column=0, padx=20, pady=0)




###### FRAME DE TELEMETRIA

frameTelemetriaSuperior = tkinter.Frame(frameTelemetria)
frameTelemetriaSuperior.grid_columnconfigure(1, weight=2)
frameTelemetriaSuperior.grid(row=0, column=0, sticky="nsew")

frameTelemetriaInferior = tkinter.Frame(frameTelemetria)
frameTelemetriaInferior.grid_columnconfigure(4, weight=1)
frameTelemetriaInferior.grid_rowconfigure(2, weight=1)
frameTelemetriaInferior.grid(row=1, column=0, sticky="nsew")

frameTelemetriaEsquerdo = tkinter.Frame(frameTelemetriaSuperior)
frameTelemetriaEsquerdo.grid_columnconfigure(0, weight=1)
frameTelemetriaEsquerdo.grid(row=0, column=0, sticky="nsew")

frameTelemetriaDireito = tkinter.Frame(frameTelemetriaSuperior)
frameTelemetriaDireito.grid_columnconfigure(0, weight=1)
frameTelemetriaDireito.grid(row=0, column=1, sticky="nsew")

frameAceleracao = tkinter.Frame(frameTelemetriaInferior)
frameAceleracao.grid_rowconfigure(2, weight=1)
frameAceleracao.grid(row=0, column=0, sticky="nsew")

frameAngulo = tkinter.Frame(frameTelemetriaInferior)
frameAngulo.grid_rowconfigure(2, weight=1)
frameAngulo.grid(row=1, column=0, sticky="nsew")

###########

velocidadeLabel = tkinter.Label(frameTelemetriaEsquerdo, text="Velocidade: 0 km/h", font=fonteTitulo, image=imagemVelocidade, compound="top")
velocidadeLabel.grid(row=0, column=0, padx=20, pady=20)

rpmLabel = tkinter.Label(frameTelemetriaEsquerdo, text="RPM: 0", font=fonteTitulo, image=imagemRpm, compound="top")
rpmLabel.grid(row=1, column=0, padx=20, pady=5)

rpmProgressBar = ttk.Progressbar(frameTelemetriaEsquerdo, orient="horizontal", length=200)
rpmProgressBar.grid(column=0, row=2, padx=10, pady=0)

temperaturaLabel = tkinter.Label(frameTelemetriaEsquerdo, text="Temperatura: 0 ºC", font=fonteTitulo, image=imagemTemperatura, compound="top")
temperaturaLabel.grid(row=3, column=0, padx=20, pady=20)

temperaturaAviso = tkinter.Label(frameTelemetriaEsquerdo, text="OK", font=fonteTitulo, fg="green")
temperaturaAviso.grid(row=4, column=0, padx=20, pady=0)

bateriaLabel = tkinter.Label(frameTelemetriaEsquerdo, text="Bateria: 0.0 V", font=fonteTitulo, image=imagemBateria, compound="top")
bateriaLabel.grid(row=5, column=0, padx=20, pady=20)

bateriaAviso = tkinter.Label(frameTelemetriaEsquerdo, text="OK", font=fonteTitulo, fg="green")
bateriaAviso.grid(row=6, column=0, padx=20, pady=0)

freioLabel = tkinter.Label(frameTelemetriaEsquerdo, text=("   Freio: Desativado"), font=fonteTitulo, image=imagemFreio, compound="left")
freioLabel.grid(row=7, column=0, padx=20, pady=50)

################

aceleracaoxLabel = tkinter.Label(frameTelemetriaInferior, text=("Aceleração X: " + str(aceleracaoX) + " G"), font=fonteTitulo, compound="left")
aceleracaoxLabel.grid(row=0, column=0, padx=20, pady=20)

aceleracaoYLabel = tkinter.Label(frameTelemetriaInferior, text=("Aceleração Y: " + str(aceleracaoY) + " G"), font=fonteTitulo, compound="left")
aceleracaoYLabel.grid(row=0, column=1, padx=20, pady=20)

aceleracaoZLabel = tkinter.Label(frameTelemetriaInferior, text=("Aceleração Z: " + str(aceleracaoZ) + " G"), font=fonteTitulo, compound="left")
aceleracaoZLabel.grid(row=0, column=2, padx=20, pady=20)

anguloXLabel = tkinter.Label(frameTelemetriaInferior, text=("Ângulo X: " + str(anguloX) + "º"), font=fonteTitulo, compound="left")
anguloXLabel.grid(row=1, column=0, padx=20, pady=20)

anguloYLabel = tkinter.Label(frameTelemetriaInferior, text=("Ângulo Y: " + str(anguloY) + "º"), font=fonteTitulo, compound="left")
anguloYLabel.grid(row=1, column=1, padx=20, pady=20)

anguloZLabel = tkinter.Label(frameTelemetriaInferior, text=("Ângulo Z: " + str(anguloZ) + "º"), font=fonteTitulo, compound="left")
anguloZLabel.grid(row=1, column=2, padx=20, pady=20)

velGPSLabel = tkinter.Label(frameTelemetriaInferior, text=("Velocidade GPS: " + str(velocidadeGPS) + " km/h"), font=fonteTitulo, compound="left")
velGPSLabel.grid(row=0, column=3, padx=20, pady=20)

botaoBox = tkinter.Button(frameTelemetriaInferior, bg="blue" , text="Chamar BOX", font=fonteTitulo, command=eventoBotaoBox, fg="white")
botaoBox.grid(row=1, column=3, padx=20, pady=20)



###### Frame Log

botaoExportar = tkinter.Button(frameLog, text="Exportar para Excel", command=eventoExportarExcel)
botaoExportar.grid(row=0, column=0, padx=50, pady=100, sticky="we")




###### Funções de Evento do Código

def selecionarFrame(nome):
    
    if nome == "conexao":
        
        frameConexao.grid(row=0, column=1, sticky="nsew")

        global serialInst
        global ports
        global portList

        #serialInst = serial.Serial()

        #ports = serial.tools.list_ports.comports()
        #portList = []

        #for onePort in ports:
        #    portList.append(str(onePort))

        #portaCOMSelector = tkinter.OptionMenu(frameConexao, varPortaCOM, *portList, command=eventoSelectCOM)
        #portaCOMSelector.grid(row=4, column=0, padx=20, pady=10)

    else:
        frameConexao.grid_forget()

    
    if nome == "telemetria":
        frameTelemetria.grid(row=0, column=1, sticky="nsew")
    else:
        frameTelemetria.grid_forget()

    if nome == "log":
        frameLog.grid(row=0, column=1, sticky="nsew")
    else:
        frameLog.grid_forget()



def eventoBotaoTelemetria():
    selecionarFrame("telemetria")
    return

def eventoBotaoConexao():
    selecionarFrame("conexao")
    return

def eventoBotaoLog():
    selecionarFrame("log")
    return






###### Threads

def lerSerial():
    
    global textoRecebido
    global velocidadeAtual
    global rpmAtual
    global temperaturaAtual
    global freioAtual
    global bateriaAtual

    global aceleracaoX
    global aceleracaoY
    global aceleracaoZ

    global anguloX
    global anguloY
    global anguloZ

    global velocidadeGPS

    global box_estado
    global box_enviar

    if statusConexao == False:
        return
    
    serialTexto = serialInst.readline().decode('latin-1')

    texto = serialTexto

    hoje = datetime.datetime.now()
    horario = hoje.strftime("%H:%M:%S.%f")
    horario = horario[0:11]
    horario_graf = horario[0:8]
    dataTempo.append(horario_graf)



    textoRecebido.insert("0.0", horario + " -> " + texto)


    # Formato da mensagem: V**R***F*T+****B***
    padrao_formato = r'^V\d+R\d+F\d+T[+-]\d+B\d+'

    if re.search("box", texto, re.IGNORECASE):
        if re.search("on", texto, re.IGNORECASE):
            box_estado = True
        elif re.search("off", texto, re.IGNORECASE):
            box_estado = False

    elif re.match(padrao_formato, texto):

        numeros = re.findall(r'\d+', texto)

        velocidadeAtual = int(numeros[0])
        dataVel.append(velocidadeAtual)

        rpmAtual = int(numeros[1])*10
        dataRPM.append(rpmAtual)

        freioAtual = bool(numeros[2])

        dataFreio.append(freioAtual)

        temperaturaAtual = float(numeros[3])/10
        if "T-" in texto:
            temperaturaAtual = -1*temperaturaAtual
        dataTemperatura.append(temperaturaAtual)

        bateriaAtual = float(numeros[4])/10
        dataBateria.append(bateriaAtual)

    else:
        print("String invalida")
        print(texto)

    #rpmAtual = int(texto[texto.index("R") + 1: 4])*10
    #dataRPM.append(rpmAtual)

    #velocidadeAtual = int(texto[4 : 6])
    #dataVel.append(velocidadeAtual)

    #temperaturaString = texto[6 : 9]

    #if(temperaturaString.find("000")!=-1):
    #    temperaturaString = "000"
    #else:
    #    temperaturaAtual = int(temperaturaString)


    #dataTemperatura.append(temperaturaAtual)

    #bateriaAtual = (float(texto[9 : 12]))/10
    #dataBateria.append(bateriaAtual)


    #freio_string = texto[12]

    #if freio_string == "0":
    #    freioAtual = False
    #else:
    #    freioAtual = True

    #dataFreio.append(freioAtual)

    #box_string = texto[13]

    #if box_string == "0":
    #    box_estado = False
    #else:
    #    box_estado = True

    if box_enviar == True:
        box_enviar = False
        text = "BOX"

        serialInst.write(text.encode('utf-8'))


    #aceleracaoX = float(texto[texto.index("x") + 1 : texto.index("y")])
    #dataAccX.append(aceleracaoX)
    #aceleracaoY = float(texto[texto.index("y") + 1 : texto.index("z")])
    #dataAccY.append(aceleracaoY)
    #aceleracaoZ = float(texto[texto.index("z") + 1 : texto.index("X")])
    #dataAccZ.append(aceleracaoZ)

    #anguloX = float(texto[texto.index("X") + 1 : texto.index("Y")])
    #dataAngX.append(anguloX)
    #anguloY = float(texto[texto.index("Y") + 1 : texto.index("Z")])
    #dataAngY.append(anguloY)
    #anguloZ = float(texto[texto.index("Z") + 1 : texto.index("G")])
    #dataAngZ.append(anguloZ)

    #velocidadeGPS = int(texto[texto.index("G") + 1 : len(texto) - 1])
    #dataVelGPS.append(velocidadeGPS)
        
    return


def atualizar():

    global textoRecebido
    global velocidadeAtual
    global rpmAtual
    global temperaturaAtual
    global freioAtual
    global bateriaAtual

    global aceleracaoX
    global aceleracaoY
    global aceleracaoZ
    global anguloX
    global anguloY
    global anguloZ

    global velocidadeGPS

    global box_estado

    #print("Thread" + str(temperaturaAtual) + " " + str(bateriaAtual) + " " + str(freioAtual))

    #print("Atualização: V" + str(velocidadeAtual) + " R" + str(rpmAtual) + " T" + str(temperaturaAtual) + " B" + str(bateriaAtual) + " F" + str(freioAtual))

    velocidadeLabel.configure(text = ("Velocidade" + str(velocidadeAtual) + " km/h"))
    rpmLabel.configure(text=("RPM" + str(rpmAtual)))
    rpmProgressBar['value'] = (rpmAtual/4000)*100

    temperaturaLabel.configure(text = ("Temperatura: " + str(temperaturaAtual) + " ºC"))
    bateriaLabel.configure(text = ("Bateria: " + str(bateriaAtual) + " V"))

    aceleracaoxLabel.configure(text = ("Aceleração X: " + str(aceleracaoX) + " G"))
    aceleracaoYLabel.configure(text = ("Aceleração Y: " + str(aceleracaoY) + " G"))
    aceleracaoZLabel.configure(text = ("Aceleração Z: " + str(aceleracaoZ) + " G"))

    anguloXLabel.configure(text=("Ângulo X: " + str(anguloX) + "º"))
    anguloYLabel.configure(text=("Ângulo Y: " + str(anguloY) + "º"))
    anguloZLabel.configure(text=("Ângulo Z: " + str(anguloZ) + "º"))

    botaoBox.configure(bg="red" if box_estado == True else "blue", text="Cancelar Box" if box_estado == True else "Chamar Box", fg="white")

    velGPSLabel.configure(text=("Velocidade GPS: " + str(velocidadeGPS) + " km/h"))

    if temperaturaAtual > 75:
        temperaturaAviso.configure(fg="red", text="ALERTA - ALTA")
    else:
        temperaturaAviso.configure(fg="green", text="OK")

    if bateriaAtual < 12:
        bateriaAviso.configure(fg="red", text="Alerta")
    else:
        bateriaAviso.configure(fg="green", text="OK")

    if freioAtual == True:
        freioLabel.configure(text="   Freio: Ativado")
    else:
        freioLabel.configure(text = "   Freio: Desativado")

    return


def animacaoGraficos(self):

    dataVelGrafico = dataVel[-60:]
    dataRPMGrafico = dataRPM[-60:]
    dataTempGrafico = dataTemperatura[-60:]
    dataBatGrafico = dataBateria[-60:]
    dataTempoFixo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]

    dataTempoGrafico = dataTempoFixo[-60:]

    grafVel.clear()
    grafRPM.clear()
    grafTemp.clear()
    grafBat.clear()

    grafVel.plot(dataVelGrafico, 'b')
    grafRPM.plot(dataRPMGrafico, 'b')
    grafTemp.plot(dataTempGrafico, 'b')
    grafBat.plot(dataBatGrafico, 'b')

    grafVel.set_title("Velocidade")
    grafRPM.set_title("RPM")
    grafTemp.set_title("Temperatura")
    grafBat.set_title("Bateria")

    grafVel.set_ylabel("km/h")
    grafVel.set_xlim(0, 60)
    grafVel.set_ylim(0, 55)

    grafRPM.set_ylabel("RPM")
    grafRPM.set_xlim(0, 60)
    grafRPM.set_ylim(0, 4500)

    grafTemp.set_ylabel("ºC")
    grafTemp.set_xlim(0, 60)
    grafTemp.set_ylim(0, 135)

    grafBat.set_ylabel("V")
    grafBat.set_xlim(0, 60)
    grafBat.set_yticks(range(0, 14))

    return


###### Frame De Navegação

frameNavegacaoLogo = tkinter.Label(frameNavegacao, text="", image=imagemLogo, width=200, height=100)
frameNavegacaoLogo.grid(row=0, column=0, padx=20, pady=0)

frameNavegacaoTitulo = tkinter.Label(frameNavegacao, text="Telemetria Imperador", compound="left", font=fonteTitulo)
frameNavegacaoTitulo.grid(row=1, column=0, padx=20, pady=0)

NavegacaoBotaoConexao = tkinter.Button(frameNavegacao, text=" Conexão", font=fonteTitulo, compound=tkinter.LEFT, image=imagemConexao, command=eventoBotaoConexao)
NavegacaoBotaoConexao.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

NavegacaoBotaoTelemetria = tkinter.Button(frameNavegacao, text=" Telemetria", font=fonteTitulo, compound=tkinter.LEFT, image=imagemTelemetria, command=eventoBotaoTelemetria)
NavegacaoBotaoTelemetria.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)

NavegacaoBotaoLog = tkinter.Button(frameNavegacao, text=" Log", font = fonteTitulo, compound=tkinter.LEFT, image=imagemLog, command=eventoBotaoLog)
NavegacaoBotaoLog.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)




###### Gráficos

graficos = FigureCanvasTkAgg(fGrafico, master=frameTelemetriaDireito)
graficos.draw()
graficos.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand = False)
graficos._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand = False)

ani = FuncAnimation(fGrafico, animacaoGraficos, interval=1000, blit=False, cache_frame_data=False)



###### Declaração das Threads

threadSerial = continuous_threading.PeriodicThread(1.0, lerSerial)
threadAtualizar = continuous_threading.PeriodicThread(0.5, atualizar)
threadSerial.start()
threadAtualizar.start()

janela.mainloop()

threadSerial.stop()
threadAtualizar.stop()