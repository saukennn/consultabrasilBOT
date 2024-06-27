import os
from undetected_chromedriver import Chrome, ChromeOptions as Options, WebElement, By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from typing import Tuple
from typing import Callable
from typing import List
from payment import get_qr
from time import sleep
import json
import base64
import socket

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36',
]

posts = ["POUPATEMPO ADAMANTINA","POUPATEMPO AGUAÍ","POUPATEMPO AGUDOS","POUPATEMPO ALESP","POUPATEMPO ÁLVARES MACHADO","POUPATEMPO AMERICANA","POUPATEMPO AMERICO BRASILIENSE","POUPATEMPO AMPARO","POUPATEMPO ANDRADINA","POUPATEMPO ANGATUBA","POUPATEMPO APARECIDA","POUPATEMPO APIAÍ","POUPATEMPO ARAÇARIGUAMA","POUPATEMPO ARAÇATUBA","POUPATEMPO ARAÇOIABA DA SERRA","POUPATEMPO ARARAQUARA","POUPATEMPO ARARAS","POUPATEMPO ARTUR NOGUEIRA","POUPATEMPO ARUJÁ","POUPATEMPO ASSIS","POUPATEMPO ATIBAIA","POUPATEMPO AVARÉ","POUPATEMPO BARIRI","POUPATEMPO BARRETOS","POUPATEMPO BASTOS","POUPATEMPO BATATAIS","POUPATEMPO BAURU","POUPATEMPO BEBEDOURO","POUPATEMPO BERTIOGA","POUPATEMPO BIRIGUI","POUPATEMPO BIRITIBA MIRIM","POUPATEMPO BOITUVA","POUPATEMPO BOM JESUS DOS PERDÕES","POUPATEMPO BOTUCATU","POUPATEMPO BRAGANÇA PAULISTA","POUPATEMPO BURI","POUPATEMPO CABREÚVA","POUPATEMPO CAÇAPAVA","POUPATEMPO CACHOEIRA PAULISTA","POUPATEMPO CAIEIRAS","POUPATEMPO CAJAMAR","POUPATEMPO CAJATI","POUPATEMPO CAMPINAS SHOPPING","POUPATEMPO CAMPO LIMPO PAULISTA","POUPATEMPO CÂNDIDO MOTA","POUPATEMPO CANINDÉ","POUPATEMPO CAPÃO BONITO","POUPATEMPO CAPELA DO ALTO","POUPATEMPO CAPIVARI","POUPATEMPO CARAGUATATUBA","POUPATEMPO CARAPICUÍBA","POUPATEMPO CATANDUVA","POUPATEMPO CERQUILHO","POUPATEMPO CIDADE ADEMAR","POUPATEMPO CIDADE TIRADENTES","POUPATEMPO CONCHAL","POUPATEMPO CORDEIRÓPOLIS","POUPATEMPO COSMÓPOLIS","POUPATEMPO COTIA","POUPATEMPO CRAVINHOS","POUPATEMPO CRUZEIRO","POUPATEMPO CUBATÃO","POUPATEMPO CUNHA","POUPATEMPO DESCALVADO","POUPATEMPO DIADEMA","POUPATEMPO DOIS CÓRREGOS","POUPATEMPO DRACENA","POUPATEMPO EMBU DAS ARTES","POUPATEMPO EMBU-GUAÇU","POUPATEMPO ESPÍRITO SANTO DO PINHAL","POUPATEMPO FERNANDÓPOLIS","POUPATEMPO FERRAZ DE VASCONCELOS","POUPATEMPO FRANCA","POUPATEMPO FRANCISCO MORATO","POUPATEMPO FRANCO DA ROCHA","POUPATEMPO GARÇA","POUPATEMPO GUAPIAÇU","POUPATEMPO GUARÁ","POUPATEMPO GUARARAPES","POUPATEMPO GUARAREMA","POUPATEMPO GUARATINGUETA","POUPATEMPO GUARIBA","POUPATEMPO GUARUJÁ","POUPATEMPO GUARULHOS","POUPATEMPO HORTOLÂNDIA","POUPATEMPO IBATÉ","POUPATEMPO IBITINGA","POUPATEMPO IBIÚNA","POUPATEMPO IGARAPAVA","POUPATEMPO IGUAPE","POUPATEMPO INDAIATUBA","POUPATEMPO IPERÓ","POUPATEMPO IRACEMÁPOLIS","POUPATEMPO ITANHAÉM","POUPATEMPO ITAPECERICA DA SERRA","POUPATEMPO ITAPETININGA","POUPATEMPO ITAPEVA","POUPATEMPO ITAPIRA","POUPATEMPO ITÁPOLIS","POUPATEMPO ITAQUAQUECETUBA","POUPATEMPO ITAQUERA","POUPATEMPO ITARARÉ","POUPATEMPO ITATIBA","POUPATEMPO ITATINGA","POUPATEMPO ITIRAPINA","POUPATEMPO ITU","POUPATEMPO ITUVERAVA","POUPATEMPO JABOTICABAL","POUPATEMPO JACAREÍ","POUPATEMPO JAGUARIÚNA","POUPATEMPO JAHU","POUPATEMPO JALES","POUPATEMPO JANDIRA","POUPATEMPO JARINU","POUPATEMPO JOSÉ BONIFÁCIO","POUPATEMPO JUNDIAÍ","POUPATEMPO JUNQUEIRÓPOLIS","POUPATEMPO LAPA","POUPATEMPO LARANJAL PAULISTA","POUPATEMPO LENÇÓIS PAULISTA","POUPATEMPO LIMEIRA","POUPATEMPO LINS","POUPATEMPO LORENA","POUPATEMPO LOUVEIRA","POUPATEMPO LUCÉLIA","POUPATEMPO MAIRIPORÃ","POUPATEMPO MARÍLIA","POUPATEMPO MARTINÓPOLIS","POUPATEMPO MATÃO","POUPATEMPO MAUÁ","POUPATEMPO MIGUELÓPOLIS","POUPATEMPO MIRANDÓPOLIS","POUPATEMPO MIRASSOL","POUPATEMPO MOCOCA","POUPATEMPO MOGI DAS CRUZES","POUPATEMPO MOGI MIRIM","POUPATEMPO MOGI-GUAÇU","POUPATEMPO MONGAGUÁ","POUPATEMPO MONTE ALTO","POUPATEMPO MONTE APRAZÍVEL","POUPATEMPO MONTE MOR","POUPATEMPO NAZARÉ PAULISTA","POUPATEMPO NEVES PAULISTA","POUPATEMPO NOVA GRANADA","POUPATEMPO NOVA ODESSA","POUPATEMPO NOVO HORIZONTE","POUPATEMPO OLÍMPIA","POUPATEMPO ORLÂNDIA","POUPATEMPO OSASCO","POUPATEMPO OSVALDO CRUZ","POUPATEMPO OURINHOS","POUPATEMPO PALMITAL","POUPATEMPO PARAGUAÇU PAULISTA","POUPATEMPO PARANAPANEMA","POUPATEMPO PAULÍNIA","POUPATEMPO PEDERNEIRAS","POUPATEMPO PEDREIRA","POUPATEMPO PENÁPOLIS","POUPATEMPO PEREIRA BARRETO","POUPATEMPO PIEDADE","POUPATEMPO PINDAMONHANGABA","POUPATEMPO PIQUETE","POUPATEMPO PIRACICABA","POUPATEMPO PIRAJUÍ","POUPATEMPO PIRAPOZINHO","POUPATEMPO PIRASSUNUNGA","POUPATEMPO PITANGUEIRAS","POUPATEMPO POÁ","POUPATEMPO PONTAL","POUPATEMPO PORTO FELIZ","POUPATEMPO PORTO FERREIRA","POUPATEMPO POTIM","POUPATEMPO PRADÓPOLIS","POUPATEMPO PRAIA GRANDE","POUPATEMPO PRESIDENTE EPITÁCIO","POUPATEMPO PRESIDENTE PRUDENTE","POUPATEMPO PRESIDENTE VENCESLAU","POUPATEMPO PROMISSÃO","POUPATEMPO REGENTE FEIJÓ","POUPATEMPO REGISTRO","POUPATEMPO RIBEIRÃO PIRES","POUPATEMPO RIBEIRÃO PRETO","POUPATEMPO RIO CLARO","POUPATEMPO RIO DAS PEDRAS","POUPATEMPO SALTO","POUPATEMPO SANTA BÁRBARA D`OESTE","POUPATEMPO SANTA CRUZ DAS PALMEIRAS","POUPATEMPO SANTA CRUZ DO RIO PARDO","POUPATEMPO SANTA FÉ DO SUL","POUPATEMPO SANTA GERTRUDES","POUPATEMPO SANTA ISABEL","POUPATEMPO SANTA RITA DO PASSA QUATRO","POUPATEMPO SANTA ROSA DE VITERBO","POUPATEMPO SANTANA DE PARNAÍBA","POUPATEMPO SANTO AMARO","POUPATEMPO SANTO ANASTÁCIO","POUPATEMPO SANTO ANDRÉ","POUPATEMPO SANTO ANTONIO DE POSSE","POUPATEMPO SANTOS","POUPATEMPO SÃO BERNARDO DO CAMPO","POUPATEMPO SÃO CARLOS","POUPATEMPO SÃO JOÃO DA BOA VISTA","POUPATEMPO SÃO JOAQUIM DA BARRA","POUPATEMPO SÃO JOSÉ DO RIO PARDO","POUPATEMPO SÃO JOSÉ DO RIO PRETO","POUPATEMPO SÃO JOSÉ DOS CAMPOS","POUPATEMPO SÃO MANUEL","POUPATEMPO SÃO MIGUEL ARCANJO","POUPATEMPO SÃO PEDRO","POUPATEMPO SÃO ROQUE","POUPATEMPO SÃO VICENTE","POUPATEMPO SÉ","POUPATEMPO SERRA NEGRA","POUPATEMPO SERRANA","POUPATEMPO SERTÃOZINHO","POUPATEMPO SOCORRO","POUPATEMPO SOROCABA","POUPATEMPO SUMARÉ","POUPATEMPO SUZANO","POUPATEMPO TABATINGA","POUPATEMPO TABOÃO DA SERRA","POUPATEMPO TAMBAÚ","POUPATEMPO TANABI","POUPATEMPO TAQUARITINGA","POUPATEMPO TAQUARITUBA","POUPATEMPO TATUÍ","POUPATEMPO TAUBATÉ","POUPATEMPO TEODORO SAMPAIO","POUPATEMPO TIETÊ","POUPATEMPO TREMEMBÉ","POUPATEMPO TUPÃ","POUPATEMPO TUPI PAULISTA","POUPATEMPO UBATUBA","POUPATEMPO VALINHOS","POUPATEMPO VALPARAÍSO","POUPATEMPO VARGEM GRANDE DO SUL","POUPATEMPO VÁRZEA PAULISTA","POUPATEMPO VINHEDO","POUPATEMPO VOTORANTIM","POUPATEMPO VOTUPORANGA"]

def shift(lst):
    if not lst:  
        return None  
    first_element = lst[0]  
    del lst[0]  
    return first_element

class Bot:
    def __init__(self):
        current_working_directory = os.getcwd()
        
        chrome_options = Options()
        # chrome_options.add_argument("--load-extension={0}".format(current_working_directory + "/capsolver_extension"))
        # chrome_options.add_argument(f"user-agent={random.choice(user_agents)}")
        # chrome_options.add_argument('--headless')  # Executa o navegador em modo headless
        # chrome_options.add_argument('--no-sandbox')  # Bypass do sandbox do Chrome
        # chrome_options.add_argument('--disable-dev-shm-usage')  # Desabilita o uso de memória compartilhada devido a problemas no Chrome em contêineres

        self.driver = Chrome(options=chrome_options, driver_executable_path="chromedriver-win64/chromedriver.exe")

        self.info = {}

    def wait(self, timeout = 20):
        return WebDriverWait(self.driver, timeout)

    def wait_and(self, elmt: Tuple[str, str], cb: Callable[[WebElement], any] = lambda x: x, *, timeout = 20):
        self.wait(timeout).until(EC.presence_of_element_located(elmt))
        return cb(self.driver.find_element(*elmt))

    def wait_and2(self, elmt: Tuple[str, str], cb: Callable[[List[WebElement]], any], *, timeout = 20):
        self.wait(timeout).until(EC.presence_of_element_located(elmt))
        return cb(self.driver.find_elements(*elmt))

    def wait_and_script(self, elmt: Tuple[str, str], script: str, *, timeout = 20):
        self.wait(timeout).until(EC.presence_of_element_located(elmt))
        return self.driver.execute_script(script)

    def click(elmt: WebElement):
        elmt.click()

    def parse_date(elmt: List[WebElement]):
        return list(map(lambda e: { "day": e.get_attribute("day"), "month": e.get_attribute("month"), "year": e.get_attribute("year") }, filter(lambda e: "disabled" not in e.get_attribute('class'), elmt)))

    def get_hour(elmt: List[WebElement]):
        return list(map(lambda e: e.text, elmt))

    def info_to_list(elmt: List[WebElement]):
        return list(map(lambda e: e.get_attribute("placeholder"), elmt))

    def in_login(self):
        return "https://sso.acesso.gov.br/login" in self.driver.current_url

    def login(self, cpf: str, passwd: str):
        self.info["cpf"] = cpf
        self.info["passwd"] = passwd

        while True:
            # self.wait().until(EC.visibility_of_element_located((By.ID, "capsolver-solver-tip-button")))
            self.wait_and_script((By.ID, "accountId"), f"document.getElementById('accountId').value = '{cpf}'")
            sleep(2)
            self.driver.find_element(value="enter-account-id").click()
            sleep(1)
            # self.wait_and_script((By.ID, "capsolver-solver-tip-button"), f"document.querySelector('#capsolver-solver-tip-button').click()")

            try:
                # self.driver.switch_to.frame(self.driver.find_elements(By.TAG_NAME, "iframe")[1])
                # self.driver.execute_script("Array.from(document.querySelectorAll('div.option span')).filter(e => e.innerText == 'English')[0].parentElement.click()")
                # self.driver.switch_to.default_content()

                # self.wait().until(EC.element_attribute_to_include((By.CSS_SELECTOR, "iframe"), "data-hcaptcha-response"))
                # while True:
                #     frame = self.driver.find_element(By.CSS_SELECTOR, "iframe")
                #     response = frame.get_attribute("data-hcaptcha-response")
                #     if len(response) > 100:
                #         break
                #     sleep(1)
                #     print("Waiting for captcha solution..")

                # form = self.driver.find_element(By.CSS_SELECTOR, ".interface-user .button-submit.button")
                # form.submit()
                
                self.wait_and_script((By.ID, "password"), f"document.getElementById('password').value = '{passwd}'")
                self.driver.find_element(value="submit-button").click()
                break
            except Exception as _:
                self.driver.refresh()
                
                continue

    def start(self):
        self.driver.get('https://www.poupatempo.sp.gov.br/wps/portal/poupatempoTaOn/servicos/redirectServicoRota?idServico=0EB2C51D-B5C2-49CC-90E7-0DEAD77917FA')

    def get_link_via_rg(self):
        # self.wait_and((By.PARTIAL_LINK_TEXT, "via do RG"), Bot.click)
        self.wait_and_script((By.CSS_SELECTOR, "a[onClick*=servico-agendamento]"), "document.querySelector('a[onClick*=servico-agendamento]').click()")

    def skip(self):
        self.wait_and((By.CSS_SELECTOR, "a[title='Agendamento individual']"), Bot.click)
        self.wait_and((By.CSS_SELECTOR, "a[title*='Posto em que deseja ser atendido']"), Bot.click)

    def select_post(self, post: str):
        self.info["post"] = post

        self.wait_and((By.CSS_SELECTOR, "input[type=search][aria-controls=buscaPostoWcm]"), lambda e: e.send_keys(post))
        self.wait_and((By.PARTIAL_LINK_TEXT, post), Bot.click)

    def get_date(self):
        list1 = None
        try:
            list1 = self.wait_and2((By.CSS_SELECTOR, "td[day][month][year]"), Bot.parse_date)
        except Exception as err:
            return "sem data"
            
        self.driver.execute_script("document.querySelector(\"div[role='period']\").nextElementSibling.click()")
        sleep(1)
        list2 = self.wait_and2((By.CSS_SELECTOR, "td[day][month][year]"), Bot.parse_date)
        self.driver.execute_script("document.querySelector(\"div[role='period']\").nextElementSibling.click()")
        sleep(1)
        return list1 + list2 + self.wait_and2((By.CSS_SELECTOR, "td[day][month][year]"), Bot.parse_date)

    def select_date(self, date):
        self.info["date"] = date

        while True:
            month = int(self.wait_and((By.CSS_SELECTOR, "div.datepicker[month]"), lambda e: e.get_attribute("month")))
            year = int(self.wait_and((By.CSS_SELECTOR, "div.datepicker[year]"), lambda e: e.get_attribute("year")))

            if month == date["month"] and year == date["year"]:
                self.wait_and_script((By.CSS_SELECTOR, f"td[day='{date["day"]}'][month='{date["month"]}'][year='{date["year"]}']:not(.disabled)"), f"document.querySelector('td[day=\"{date["day"]}\"][month=\"{date["month"]}\"][year=\"{date["year"]}\"]:not(.disabled) div').click()")
                break

            if date["month"] > month or date["year"] > year:
                self.driver.execute_script("document.querySelector(\"div[role='period']\").nextElementSibling.click()")
            else:
                self.driver.execute_script("document.querySelector(\"div[role='period']\").previousElementSibling.click()")

            sleep(2)

    def get_hours(self):
        return self.wait_and2((By.CSS_SELECTOR, "a[onclick*=horario]"), Bot.get_hour)

    def select_hour(self, hour):
        self.info["hour"] = hour

        return self.wait_and((By.PARTIAL_LINK_TEXT, hour), Bot.click)

    def get_info(self):
        content = self.wait_and2((By.CSS_SELECTOR, ".area_form_cad input"), Bot.info_to_list)
        self.info["name"] = shift(content)
        self.info["post"] = shift(content)
        self.info["addr"] = shift(content)
        shift(content)
        shift(content)
        self.info["date-hour"] = shift(content)
        phone = self.wait_and((By.CSS_SELECTOR, ".area_form_cad input[id*=inputCel]"), lambda e: e.get_attribute("value"))

        return { "name": self.info["name"], "post": self.info["post"], "addr": self.info["addr"], "date": self.info["date-hour"], "phone": phone }

    def set_info(self, rg, naturalidade, email, phone = None):
        self.info["rg"] = rg
        self.info["naturalidade"] = naturalidade
        self.info["phone"] = phone
        self.info["email"] = email
        self.info["status"] = False
        self.info["file_name"] = f"{self.info["cpf"]} - {self.info["name"]} {self.info["date-hour"].replace("/", "-").replace(":", "-")}"

        with open(f"./save/{self.info["file_name"]}.json", "w+t") as f:
            f.write(json.dumps(self.info))
        
        self.wait_and_script((By.CSS_SELECTOR, ".area_form_cad"), f'document.querySelector(".area_form_cad input[id*=tipoRG\\\\:{rg}]").click()')

        sleep(1)

        self.wait_and_script((By.CSS_SELECTOR, ".modal-poupinha button.btn"), f'document.querySelector(".modal-poupinha button.btn").click()')
        
        sleep(1)

        self.wait_and_script((By.CSS_SELECTOR, ".area_form_cad"), f'document.querySelector(".area_form_cad input[id*=naturalidade\\\\:{naturalidade}]").click()')

        if phone:
            self.driver.execute_script(f'document.querySelector(".area_form_cad input[id*=inputCel]").value = "{phone}"')

    def finish(self):
        self.wait_and((By.CSS_SELECTOR, "a[id*=btnProsseguirAgendamento]"), Bot.click)
        html = self.wait_and_script((By.CSS_SELECTOR, "div.protocolo"), 'return document.querySelector(".protocolo").innerHTML')
        
        self.info["html"] = html
        self.info["status"] = True

        with open(f"./save/{self.info["file_name"]}.json", "w+t") as f:
            f.write(json.dumps(self.info))
            
        resp = get_qr(0.1, self.info["email"], base64.urlsafe_b64encode(self.info["file_name"].encode()).decode())
        resp["info"] = self.info
        resp["html"] = html

        return resp

    def close(self):
        self.driver.quit()

def bot_handler(socket: socket):
    while True:
        bot = Bot()
        bot.start()
        bot.get_link_via_rg()
        
        is_logged = False
        post = False
        setInfo = False
        date = {}
        hour = ""

        while True:
            try:
                message = json.loads(socket.recv(4096).decode('utf-8'))

                if isinstance(message, str):
                    if message == "quit":
                        bot.close()
                        return
                
                if (not is_logged and (message["cpf"] and message["pass"])):
                    bot.login(message["cpf"], message["pass"])
                    socket.sendall(json.dumps(not bot.in_login()).encode())
                    if bot.in_login():
                        bot.start()
                        bot.get_link_via_rg()

                        continue

                    is_logged = True
                    bot.skip()

                if message["post"] and not post:
                    post = True

                    try:
                        bot.select_post(message["post"])
                    except:
                        socket.sendall(json.dumps("exists").encode())
                        break


                    dates = bot.get_date()
                    socket.sendall(json.dumps(dates).encode())

                    continue

                if message["date"] and not date:
                    splited = message["date"].split("-")
                    date = {
                        "year": int(splited[0]),
                        "month": int(splited[1]) - 1,
                        "day": int(splited[2])
                    }
                    bot.select_date(date)

                    hours = bot.get_hours()
                    socket.sendall(json.dumps(hours).encode())

                    continue

                if message["hour"] and not hour:
                    hour = message["hour"]
                    bot.select_hour(hour)

                    info = bot.get_info()
                    socket.sendall(json.dumps(info).encode())

                    continue

                if message["orig"] and message["option"] and message["email"] and not setInfo:
                    resp = dict()
                    setInfo = {
                        "rg": message["option"],
                        "naturalidade": message["orig"],
                        "email": message["email"],
                        "phone": None
                    }

                    if "phone" in message:
                        setInfo["phone"] = message["phone"]

                    while True:
                        bot.set_info(setInfo["rg"], setInfo["naturalidade"], setInfo["email"], setInfo["phone"])
                        sleep(1)

                        try:
                            resp = bot.finish()
                        except:
                            continue

                        break

                    socket.sendall(json.dumps(resp).encode())

                    break
            
            except Exception as err:
                print(err)

                break

        socket.sendall(json.dumps("timeout").encode())
        bot.close()

if __name__ == "__main__":
    host = 'portalagendabrasil.store'
    port = 8766 

    # Criação do socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conexão com o servidor
        client_socket.connect((host, port))
        print("Conexão estabelecida com sucesso.")

        bot_handler(client_socket)

    except Exception as e:
        print("Erro ao conectar ou enviar/receber dados:", e)

    finally:
        # Fechar o socket
        client_socket.close()