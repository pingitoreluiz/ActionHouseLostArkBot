from discord.ext import commands
import discord,csv,requests,time,os

token=''

# manutenção/exclusão do arquivo para evitar acumulo desnecessario de arquivos .csv
def manutencao_tabela(file):
    print("Excluindo o arquivo csv")
    os.remove(file)
    print("O arquivo foi excluido")
    

bot=commands.Bot(command_prefix="!",intents=discord.Intents.all())

bot.event
async def on_ready():
    print("O bot esta online")
    
@bot.command()
async def check(ctx,arg):
    
    #Define os parametros de criação do arquivo ao mesmo
    hora=time.localtime()
    url = "https://www.lostarkmarket.online/api/export-market-live/South America?categories=Enhancement Material&format=csv"
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    arquivotext="LostarkAH{ano}{mes}{dia}{sec}.csv".format(ano=hora.tm_year, mes=hora.tm_mon,dia= hora.tm_mday, sec=hora.tm_sec)
    f = open(arquivotext, "x")
    f.write(response.text)
    f.close()

    print("O arquivo foi criado")
    
    # Abre o arquivo .csv e extrai as informações necessarias, apos checar o item que o usuario precisa
    with open(arquivotext, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if row[1]==arg: 
                   
                #Criação do embed e alocação dos campos seus campos
                embed=discord.Embed(title=row[2])
                embed.set_thumbnail(url=row[3])
                embed.add_field(name='Recent Price:',value= '{rp}g'.format(rp=row[6]))
                embed.add_field(name='Lowest Price',value= '{lp}g'.format(lp=row[5]))
                infile.close()
                
                # o bot manda a mensagem em formato embed com as informações requisitadas
                await ctx.send(embed=embed)
                manutencao_tabela(arquivotext)
                break
            else:
                await ctx.send('O ID:{id} não foi encontrado na tabela'.format(id=arg))
                infile.close()
                manutencao_tabela(arquivotext)
                break
                
   
    
@bot.command()
async def ajuda(ctx,user:discord.Member=None):
    #o bot usa .csv para fazer uma lista de ajuda para o usuario que esta em duvida sobre o item que quer consultar
    arquivo='listaitem.csv'
    mydict={}
    user=ctx.author
    
    embed=discord.Embed(title='Lista de items')
    
    # Abre o arquivo e transforma os dados num dicionario para uma facil execução do embed
    with open(arquivo, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if row[2] != 'name':
                embed.add_field(name=row[2],value= row[1], inline=False)
                embed.set_thumbnail(url='https://www.lostarkmarket.online/assets/item_icons/tailoring-basic-design.webpw')
        
    # Cria um embed com a lista de items e seus respectivos ids

    await user.send(embed=embed)

bot.run(token)