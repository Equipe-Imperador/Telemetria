######################
#
# Telemetria.py - Arquivo para fase 4 do PS da equipe Baja Imperador
# Autor: Rafael Eijy Ishikawa Rasoto - RA: 2004585
# GitHub: IshikawaRasoto
# E-mail para contato: rafaelrasoto@alunos.utfpr.edu.br || ishikawarasoto@gmail.com
#
#
# É necessário alterar o diretório do Excel na função evento_exportar_excel
######################

import customtkinter #necessita baixar biblioteca customtkinter
import os
from PIL import Image #necessita baixar
import serial.tools.list_ports #necessita baixar pyserial
import threading
import continuous_threading #necessita baixar biblioteca continuous_threading
import datetime
import numpy #baixar numpy
import matplotlib.pyplot as plt #necessita baixar matplotlib
from drawnow import * #necessita baixar drawnow
#import matplotlib.animation as animation
import pandas as pd #necessita baixar pandas
#baixar openpyxl


serialInst = serial.Serial()

ports = serial.tools.list_ports.comports()
portList = []

for onePort in ports:
    portList.append(str(onePort))

customtkinter.set_default_color_theme("dark-blue")

#variavies porta COM ##################

status_conexao = False
baudRate = 9600
global portaCOM 
portaCOM = "COM3"


# variáveis do carro ################################

velocidade_atual = 0 
rpm_atual = 0
freio_atual = False
temperatura_atual = False
bateria_atual = False


# variáveis gráficos ################################

dataVel = []
dataRPM = []
dataTempo = []
#FigVel = plt.figure()
#velx = figVel.add_subplot(111)


def evento_baudRate_selector(baudRate_recebido):
    print("Baud Rate recebido: " + baudRate_recebido)
    global baudRate
    baudRate = int(baudRate_recebido)
    print("Variável BaudRate: " + str(baudRate))

def evento_COM_selector(COM_recebida):
    global portaCOM
    for i in range(0, len(portList)):
        if portList[i] == COM_recebida:
            print("COM recebida:" + portList[i][0:4])
            portaCOM = portList[i][0:4]
    

def evento_botao_conectar():
    global status_conexao
    status_conexao = True
    conectar_botao.configure(text = "Desconectar", command=evento_botao_desconectar)
    status_conexao_label.configure(text = "Conectado", fg_color="green")
    serialInst.baudrate = baudRate
    serialInst.port = portaCOM
    serialInst.open()
        
def evento_botao_desconectar():
    global status_conexao
    status_conexao = False
    conectar_botao.configure(text = "Conectar", command=evento_botao_conectar)
    status_conexao_label.configure(text = "Desconectado", fg_color="red")
    serialInst.close()

def evento_botao_apagar():
    texto_recebido.delete("0.0", "end")

def evento_exportar_excel():
    data = {'horario': dataTempo,
            'velocidade': dataVel,
            'RPM': dataRPM}
    
    df = pd.DataFrame(data)

    df.to_excel(r'C:\Users\rraso\OneDrive\Documentos\UTFPR\BAJA\Case\TelemetriaPython\XL\data.xlsx', index=False)



# Janela Principal #############################

janela = customtkinter.CTk()
janela.geometry("1280x720")
janela.title("Equipe Imperador - Software Telemetria")
janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(1, weight=1)







#Path das Imagens do Projeto################

image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")

logo_image = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "LogoDark.png")), light_image=Image.open(os.path.join(image_path, "LogoLight.png")), size=(200,100))
conexao_imagem = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "ConexaoDark.png")), light_image=Image.open(os.path.join(image_path, "ConexaoLight.png")),  size=(50,50))
telemetria_imagem = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "estatisticasDark.png")), light_image=Image.open(os.path.join(image_path, "estatisticaslight.png")),size=(50, 50))
log_imagem = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "LogDark.png")), light_image=Image.open(os.path.join(image_path, "LogLight.png")), size=(50, 50))
borracha_imagem = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "BorrachaDark.png")), light_image=Image.open(os.path.join(image_path, "BorrachaLight.png")), size=(30,30))
freio_imagem = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "freioDark.png")), light_image=Image.open(os.path.join(image_path, "freioLight.png")), size=(50,50))
temperatura_imagem = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "temperaturaDark.png")), light_image=Image.open(os.path.join(image_path, "temperaturaLight.png")), size=(50,50))
bateria_imagem = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "bateriaDark.png")), light_image=Image.open(os.path.join(image_path, "bateriaLight.png")), size=(50,50))
velocidade_imagem = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "velocidadeDark.png")), light_image=Image.open(os.path.join(image_path, "velocidadeLight.png")), size=(50,50))
rpm_imagem = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "rpmDark.png")), light_image=Image.open(os.path.join(image_path, "rpmLight.png")), size=(50,50))
conectar_imagem = customtkinter.CTkImage(Image.open(os.path.join(image_path, "conectar.png")) ,size=(25, 25))

grafico_velocidade_imagem = customtkinter.CTkImage(Image.open(os.path.join(image_path, "LogoDark.png")), size=(200,100))
grafico_rpm_imagem = customtkinter.CTkImage(Image.open(os.path.join(image_path, "LogoDark.png")), size=(200,100))



# Definição das Telas do Sistema #########################################

frame_conexao = customtkinter.CTkFrame(janela, corner_radius=0, fg_color="transparent")
frame_conexao.grid_columnconfigure(0, weight=1)
frame_conexao.grid(row=0, column=1, sticky="nsew")

frame_telemetria = customtkinter.CTkFrame(janela, corner_radius=0, fg_color="transparent")
frame_telemetria.grid_columnconfigure(2, weight=1)

frame_log = customtkinter.CTkFrame(janela, corner_radius=0, fg_color="transparent")
frame_log.grid_columnconfigure(0, weight=1)









# Frame De Conexão com o carro ############################################

status_conexao_label = customtkinter.CTkLabel(frame_conexao, fg_color=("red") if status_conexao == False else "green", text=("Desconectado") if status_conexao == False else "Conectado", text_color=("white"), corner_radius=15, font=customtkinter.CTkFont("Oswald", 20))
status_conexao_label.grid(row=0, column=0, padx=20, pady=20)

baudRate_label = customtkinter.CTkLabel(frame_conexao, fg_color="transparent", text="Baud-Rate", font=customtkinter.CTkFont("Oswald", 20))
baudRate_label.grid(row=1, column=0, padx=20, pady=0)

baudRate_selector = customtkinter.CTkOptionMenu(frame_conexao, values=["9600", "38400", "115200"], command=evento_baudRate_selector)
baudRate_selector.grid(row=2, column=0, padx=20, pady=10)

portaCOM_label = customtkinter.CTkLabel(frame_conexao, fg_color="transparent", text="Porta COM", font=customtkinter.CTkFont("Oswald", 20))
portaCOM_label.grid(row=3, column=0, padx=20, pady=0)

portaCOM_selector = customtkinter.CTkOptionMenu(frame_conexao, values=portList, command=evento_COM_selector)
portaCOM_selector.grid(row=4, column=0, padx=20, pady=10)

conectar_botao = customtkinter.CTkButton(frame_conexao, text="Conectar" if status_conexao == False else "Desconectar", image=conectar_imagem, command=evento_botao_conectar if status_conexao == False else evento_botao_desconectar)
conectar_botao.grid(row=5, column=0, padx=20, pady=10)

texto_recebido = customtkinter.CTkTextbox(frame_conexao, state="normal", font=customtkinter.CTkFont("Oswald", 12), width=800, height=300)
texto_recebido.grid(row=6, column=0, padx=20, pady=10)

apagar_botao = customtkinter.CTkButton(frame_conexao, text="Apagar", image=borracha_imagem, command=evento_botao_apagar)
apagar_botao.grid(row=7, column=0, padx=20, pady=0)

texto_comando = customtkinter.CTkTextbox(frame_conexao, state="disabled" if status_conexao == False else "normal", font=customtkinter.CTkFont("Oswald", 12), width=800, height=25)
texto_comando.grid(row=8, column=0, padx=20, pady=10)

enviar_comando_botao = customtkinter.CTkButton(frame_conexao, text="Enviar")
enviar_comando_botao.grid(row=9, column=0, padx=20, pady=0)








# Frame De Telemetria com o carro ############################################

frame_telemetria_esquerdo = customtkinter.CTkFrame(frame_telemetria, corner_radius=0, fg_color="transparent")
frame_telemetria_esquerdo.grid_columnconfigure(0, weight=1)
frame_telemetria_esquerdo.grid(row=0, column=0, sticky="nsew")

frame_telemetria_direito = customtkinter.CTkFrame(frame_telemetria, corner_radius=0, fg_color="transparent")
frame_telemetria_direito.grid_columnconfigure(0, weight=1)
frame_telemetria_direito.grid(row=0, column=1, sticky="nsew")

velocidade_label = customtkinter.CTkLabel(frame_telemetria_esquerdo, text = ("Velocidade: 0" + " km/h") , font=customtkinter.CTkFont("Impact", 24), image=velocidade_imagem, compound="top")
velocidade_label.grid(row=0, column=0, padx=20, pady=20)

rpm_label = customtkinter.CTkLabel(frame_telemetria_esquerdo, text = ("RPM: 0") , font=customtkinter.CTkFont("Impact", 24), image=rpm_imagem, compound="top")
rpm_label.grid(row=1, column=0, padx=20, pady=20)

rpm_progress_bar = customtkinter.CTkProgressBar(frame_telemetria_esquerdo, height=25, orientation="horizontal", determinate_speed=0)
rpm_progress_bar.start()
rpm_progress_bar.set(0)
rpm_progress_bar.grid(row=2, column=0, padx=20, pady=0)

temperatura_label = customtkinter.CTkLabel(frame_telemetria_esquerdo, text=("Temperatura"), font=customtkinter.CTkFont("Impact", 24), image=temperatura_imagem, compound="top")
temperatura_label.grid(row=3, column=0, padx=20, pady=20)

temperatura_aviso = customtkinter.CTkLabel(frame_telemetria_esquerdo, text="OK", font=customtkinter.CTkFont("Impact", 24), fg_color="green", corner_radius=10)
temperatura_aviso.grid(row=4, column=0, padx=20, pady=0)

bateria_label = customtkinter.CTkLabel(frame_telemetria_esquerdo, text=("Bateria"), font=customtkinter.CTkFont("Impact", 24), image=bateria_imagem, compound="top")
bateria_label.grid(row=5, column=0, padx=20, pady=20)

bateria_aviso = customtkinter.CTkLabel(frame_telemetria_esquerdo, text="OK", font=customtkinter.CTkFont("Impact", 24), fg_color="green", corner_radius=10)
bateria_aviso.grid(row=6, column=0, padx=20, pady=0)

freio_label = customtkinter.CTkLabel(frame_telemetria_esquerdo, text=("  Freio: Desativado"), font=customtkinter.CTkFont("Impact", 24), image=freio_imagem, compound="left")
freio_label.grid(row=7, column=0, padx=20, pady=50)

velocidade_grafico = customtkinter.CTkLabel(frame_telemetria_direito, image=grafico_velocidade_imagem, text="", height=100, width=200)
velocidade_grafico.grid(row=0, column=0, padx=20, pady=0)

rpm_grafico = customtkinter.CTkLabel(frame_telemetria_direito, image=grafico_rpm_imagem, text="")
rpm_grafico.grid(row=1, column=0, padx=20, pady=0)






# Frame Log ########################################

botao_exportar = customtkinter.CTkButton(frame_log, text="Exportar para Excel", command=evento_exportar_excel)
botao_exportar.grid(row=0, column=0, padx=50, pady=100, sticky="we")





# Funções de Evento Código ########################
def selecionar_frame(nome):
    frame_botao_telemetria.configure(fg_color=("gray75", "gray25") if nome == "telemetria" else "transparent")
    frame_botao_conexao.configure(fg_color=("gray75", "gray25") if nome == "conexao" else "transparent")
    frame_botao_Log.configure(fg_color=("gray75", "gray25") if nome == "log" else "transparent")

    if nome == "conexao":
        frame_conexao.grid(row=0, column=1, sticky="nsew")
        serialInst = serial.Serial()

        ports = serial.tools.list_ports.comports()
        portList = []

        for onePort in ports:
            portList.append(str(onePort))

        portaCOM_selector = customtkinter.CTkOptionMenu(frame_conexao, values=portList, command=evento_COM_selector)
        portaCOM_selector.grid(row=4, column=0, padx=20, pady=10)
    
    else:
        frame_conexao.grid_forget()
    
    if nome == "telemetria":
        frame_telemetria.grid(row=0, column=1, sticky="nsew")
    else:
        frame_telemetria.grid_forget()

    if nome == "log":
        frame_log.grid(row=0, column=1, sticky="nsew")
    else:
        frame_log.grid_forget()
    
def evento_botao_telemetria():
    selecionar_frame("telemetria")

def evento_botao_conexao():
    selecionar_frame("conexao")

def evento_botao_log():
    selecionar_frame("log")

def evento_mudar_tema(nova_aparencia):
    customtkinter.set_appearance_mode(nova_aparencia)



# Thread #########################

def lerSerial():

    global texto_recebido
    global velocidade_atual
    global rpm_atual
    global temperatura_atual
    global freio_atual
    global bateria_atual

    if status_conexao == True:

        print("tentando Imprimir Serial")

        serial_texto = serialInst.readline()

        hoje = datetime.datetime.now()
        horario = hoje.strftime("%H:%M:%S.%f")
        horario = horario[0:11]
        horario_graf = horario[0:8]
        dataTempo.append(horario_graf)

        serial_texto = serial_texto.decode("utf-8")

        texto = serial_texto
        texto_recebido.insert("0.0", horario + " -> " + texto)

        velocidade_atual = int(texto[texto.index("V") + 1: texto.index("T")])
        dataVel.append(velocidade_atual)

        rpm_atual = int(texto[texto.index("R") + 1: texto.index("V")])*10
        dataRPM.append(rpm_atual)

        temperatura_string = texto[texto.index("T") + 1: texto.index("F")]
        freio_string = texto[texto.index("F") + 1: texto.index("B")]
        bateria_string = texto[texto.index("B") + 1: len(texto) - 1]

        if temperatura_string == "0":
            temperatura_atual = False
        else:
            temperatura_atual = True

        if freio_string == "0":
            freio_atual = False
        else:
            freio_atual = True
        
        if bateria_string == "0":
            bateria_atual = False
        else:
            bateria_atual = True




        


def atualizar():
    global texto_recebido
    global velocidade_atual
    global rpm_atual
    global temperatura_atual
    global freio_atual
    global bateria_atual

    velocidade_label.configure(text= ("Velocidade: " + str(velocidade_atual) + " km/h"))
    rpm_label.configure(text="RPM: " + str(rpm_atual))

    rpm_progress_bar.set(rpm_atual/4000)

    if(rpm_atual<2500):
        rpm_progress_bar.configure(progress_color = "blue")
    elif (rpm_atual >= 2500 and rpm_atual < 3500):
        rpm_progress_bar.configure(progress_color = "green")
    else:
        rpm_progress_bar.configure(progress_color = "red")

    if temperatura_atual == True:
        temperatura_aviso.configure(fg_color="red", text="ALERTA - ALTA")
    else:
        temperatura_aviso.configure(fg_color="green", text="OK")

    if bateria_atual == True:
        bateria_aviso.configure(fg_color="red", text="ALERTA - ALTA")
    else:
        bateria_aviso.configure(fg_color="green", text="OK")

    if freio_atual == True:
        freio_label.configure(text=("  Freio: Ativado"))
    else:
        freio_label.configure(text=("  Freio: Desativado"))

    

    


def atualizar_graficos():

    dataVelGrafico = dataVel[-60:]
    dataRPMGrafico = dataRPM[-60:]

    plt.ylim(0, 60)
    plt.title("Velocidade")
    plt.grid(False)
    plt.ylabel("Km/h")
    plt.plot(dataVelGrafico)
    plt.savefig('imgs/graficoVEL.png', transparent=True)

    plt.clf()

    plt.ylim(0, 5000)
    plt.title("RPM")
    plt.grid(False)
    plt.ylabel("RPM")
    plt.plot(dataRPMGrafico)
    plt.savefig('imgs/graficoRPM.png', transparent=True)

    plt.clf()

    global grafico_velocidade_imagem
    global grafico_rpm_imagem

    grafico_velocidade_imagem = customtkinter.CTkImage(Image.open(os.path.join(image_path, "graficoVEL.png")), size=(700,350))
    velocidade_grafico.configure(image=grafico_velocidade_imagem)

    grafico_rpm_imagem = customtkinter.CTkImage(Image.open(os.path.join(image_path, "graficoRPM.png")), size=(700,350))
    rpm_grafico.configure(image=grafico_rpm_imagem)


# Frame Navegação ####################

frame_navegacao = customtkinter.CTkFrame(janela, corner_radius=0)
frame_navegacao.grid(row=0, column=0, sticky="nsew")
frame_navegacao.grid_rowconfigure(5, weight=1)

frame_navegacao_imagem = customtkinter.CTkLabel(frame_navegacao, text="", image=logo_image, compound="left", font = customtkinter.CTkFont("Impact", size=30))
frame_navegacao_imagem.grid(row=0, column=0, padx=20, pady=0)

frame_navegacao_label = customtkinter.CTkLabel(frame_navegacao, text="Software de Telemetria", compound="left", font = customtkinter.CTkFont("Impact", size=20))
frame_navegacao_label.grid(row=1, column=0, padx=20, pady=0)

frame_botao_conexao = customtkinter.CTkButton(frame_navegacao, corner_radius=0, height=100, border_spacing=10, text="Conexão", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=conexao_imagem, anchor="w", command=evento_botao_conexao, font = customtkinter.CTkFont("Impact", size=20))
frame_botao_conexao.grid(row=2, column=0, sticky="ew")

frame_botao_telemetria = customtkinter.CTkButton(frame_navegacao, corner_radius=0, height=100, border_spacing=10, text="Telemetria", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=telemetria_imagem, anchor="w", command=evento_botao_telemetria, font = customtkinter.CTkFont("Impact", size=20))
frame_botao_telemetria.grid(row=3, column=0, sticky="ew")

frame_botao_Log = customtkinter.CTkButton(frame_navegacao, corner_radius=0, height=100, border_spacing=10, text="Log", fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=log_imagem, anchor="w", command=evento_botao_log, font = customtkinter.CTkFont("Impact", size=20))
frame_botao_Log.grid(row=4, column=0, sticky="ew")

menu_tema = customtkinter.CTkOptionMenu(frame_navegacao, values=["System","Light","Dark"], command=evento_mudar_tema)
menu_tema.grid(row=6, column=0, padx=20, pady=20, sticky="s")


threadSerial = continuous_threading.PeriodicThread(0.5, lerSerial)
threadAtualizacao = continuous_threading.PeriodicThread(0.5, atualizar)
threadGraficos = continuous_threading.PeriodicThread(1.5, atualizar_graficos)
threadSerial.start()
threadAtualizacao.start()
threadGraficos.start()

#ani = animation.FuncAnimation(figVel, animacao, frames=100, fargs=(dataVel), interval=100)

#plt.show()

janela.mainloop()

threadSerial.stop()
threadAtualizacao.stop()
threadGraficos.stop()