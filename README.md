ProdamLab - Busca Diário Livre
==============================

Busca expressões dentro do Diário Oficial do município de São Paulo através da
ferramenta [DiárioLivre](http://devcolab.each.usp.br/do/).

Pacotes
-------

###ChefeDeGabinete

Busca Nomeações, Exonerações e Substituições de Chefes de Gabinetes das 
secretarias do município de São Paulo.
Faz uma busca completa até a data configurada na primeira vez e apenas busca 
informações novas nas 
execuções subsequentes

###Prodam

Busca entradas relacionadas com a *Prodam*, bem como elementos relacionados com
a administração indireta e também empresas suspensas de participação em 
licitações e impedidas de contratar com a administração.

Antes de Usar
-------------

- Renomear config.xml.template para config.xml
- Editar configurações em config.xml

Requisitos
----------

- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [Mechanize](http://wwwsearch.sourceforge.net/mechanize)
- Conta gmail válida para envio de e-mails.

Uso
---

A ferramenta possui dois modos de funcionamento:

- **Sem argumentos**: a ferramenta buscará sempre informações novas a partir da 
última execução ou *BaseDate* especificada no arquivo de configuração caso seja
a primeira vez que o aplicativo é executado. Ao final do processo um e-mail será
 enviado para os destinatários presentes no arquivo de configuração com as
entradas encontradas.
- **Com argumentos -s e -e no formato dd/mm/aaaa**: a ferramenta buscará os
registros no intervalo especificado entre *-s* e *-e*. (**ex:** main.py -s 
01/01/2014 -e 01/02/2014). Nenhum e-mail será
enviado. Apenas o log será atualizado.

Configuração
------------

Dentro do arquivo *config.xml* ou no arquivo de configuração específico de cada 
pacote, presentes no diretório Config, deve constar:

**Configuração de E-mail**

- **Username**: usuário da conta de e-mail utilizada para postar resultados;
- **Password**: senha da conta de e-mail utilizada para postar resultados;
- **From**: e-mail remetente;
- **Subject**: assunto do e-mail de resultados;
- **To**: lista de destinatários. Cada um dentro de seu respectivo **Email**;
- **Header**: cabeçalho do e-mail de resultados;
- **Footer**: rodapé do e-mail de resultados;
- **BaseDate**: especifica data de parada da ferramenta no caso da primeira
execução;

**Configuração de Rede**

- **Proxy**: endereço do proxy não autenticado da rede. Deixar em branco caso
não haja proxy;

**Configuração de Logs**

- **LogMode**: determina se o arquivo de log deve ser atualizado (*Append*) ou 
sobrescrito (*Overwrite*) após cada execução;

**Configuração de Tolerância a Erros**

- **Timeout**: tempo máximo (em segundos) de espera por dados em conexão ativa;
- **Retries**: número máximo de tentativas em caso de transbordo de tempo de 
espera;
- **TimeBetweenRetries**: intervalo (em segundos) de espera entre tentativas no
caso de transbordo do tempo de espera;

**Módulos**

- **Name**: cada pacote a ser carregado deve estar nesta lista. Os pacotes
devem ter um módulo principal *main* e uma funcção *Run* como ponto de entrada.

Desenvolvedores
---------------

A interface básica para busca no diário livre já existe. Para implementar uma 
nova busca é necessário herdar de *DlSearch* para incluir as opções de busca, de
*GenericParser* para incluir as expressões regulares que filtrarão os resultados
e herdar de  *ResponseProcessor*, implementando um método *Persist* (que 
receberá como parâmetro os grupos de interesse determinados pela expressão 
regular em *GenericParser* e deve ser responsável pela saída de dados desejada), 
*Iterate* (disparado no fim do processamento de cada doc) e 
*ProcessEnd* caso necessário.
