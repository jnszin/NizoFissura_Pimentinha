import discord
from discord import app_commands
import requests
from dotenv import load_dotenv
import os

# Carrega o conteúdo do .env
load_dotenv()

# Obtém as variáveis de ambiente
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
API_KEY = os.getenv("WEATHER_API_KEY")

class BotDiscord(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"{self.user} foi inicializado com sucesso.")

bot = BotDiscord()

# Comando de saudação
@bot.tree.command(name="olá-zépangaré", description="Primeiro comando do nizofissura")
async def ola_zepangare(interaction: discord.Interaction): 
    await interaction.response.send_message(f"Olá {interaction.user.mention}!")

# Comando de soma
@app_commands.describe(
    numero1="Primeiro número a somar",
    numero2="Segundo número a somar"
)
@bot.tree.command(name="soma", description="Somar dois números distintos")
async def soma(interaction: discord.Interaction, numero1: float, numero2: float): 
    resultado = numero1 + numero2
    await interaction.response.send_message(f"A soma de {numero1} + {numero2} é igual a {resultado}")

 # Calculo de IMC
@app_commands.describe(
    peso="Seu peso em kg (ex: 70.5)",
    altura="Sua altura em metros (ex: 1.75)"
)
@bot.tree.command(name="imc", description="Calcula o IMC com base no peso e altura fornecidos")
async def imc(interaction: discord.Interaction, peso: float, altura: float):
    if altura <= 0:
        await interaction.response.send_message("❌ Altura inválida. Deve ser maior que zero.")
        return

    imc_valor = peso / (altura ** 2)
    classificacao = ""

    if imc_valor < 18.5:
        classificacao = "Abaixo do peso"
    elif imc_valor < 25:
        classificacao = "Peso normal"
    elif imc_valor < 30:
        classificacao = "Sobrepeso"
    elif imc_valor < 35:
        classificacao = "Obesidade grau 1"
    elif imc_valor < 40:
        classificacao = "Obesidade grau 2"
    else:
        classificacao = "Obesidade grau 3 (mórbida)"

    await interaction.response.send_message(
        f"📏 **IMC Calculado:** {imc_valor:.2f}\n"
        f"📊 **Classificação:** {classificacao}"
    )
# Comando de clima
@app_commands.describe(
    cidade="Nome da cidade para ver o clima (ex: Vitória,BR)"
)

@bot.tree.command(name="clima", description="Consulta o clima de uma cidade")
async def clima(interaction: discord.Interaction, cidade: str = 'Vitória,BR'):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados = resposta.json()
        descricao = dados['weather'][0]['description'].capitalize()
        temperatura = dados['main']['temp']
        sensacao = dados['main']['feels_like']
        umidade = dados['main']['humidity']
        await interaction.response.send_message(
            f"🌤️ **Clima em {cidade}**:\n"
            f"- Descrição: {descricao}\n"
            f"- Temperatura: {temperatura}°C\n"
            f"- Sensação térmica: {sensacao}°C\n"
            f"- Umidade: {umidade}%"
        )
    else:
        await interaction.response.send_message(
            f"❌ Não consegui encontrar o clima da cidade **{cidade}** ou houve erro na API (código: {resposta.status_code})."
        )   
@bot.tree.command(name="dolar", description="Mostra a cotação atual do dólar em reais (BRL)")
async def cotacao_dolar(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        # API do AwesomeAPI
        url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
        resposta = requests.get(url, timeout=5)

        if resposta.status_code == 200:
            dados = resposta.json()
            cotacao = float(dados["USDBRL"]["bid"])
            variacao = float(dados["USDBRL"]["pctChange"])
            hora = dados["USDBRL"]["create_date"]

            await interaction.followup.send(
                f"💵 **Cotação do Dólar (USD → BRL):**\n"
                f"- Valor: R$ {cotacao:.2f}\n"
                f"- Variação: {variacao:.2f}%\n"
                f"- Atualizado em: {hora}"
            )
        else:
            await interaction.followup.send("❌ Não foi possível obter a cotação do dólar.")
    except Exception as erro:
        await interaction.followup.send(f"⚠️ Ocorreu um erro ao buscar a cotação: `{str(erro)}`")




# Inicia o bot com o token vindo do .env
bot.run(DISCORD_TOKEN)