ProdamLab - Chefes de Gabinete
==========================================

Busca Nomeações, Exonerações e Substituições de Chefes de Gabinetes das 
secretarias do município de São Paulo
 no [DiárioLivre](http://devcolab.each.usp.br/do/).
Faz uma busca completa até a data configurada na primeira vez e apenas busca 
informações novas nas 
execuções subsequentes

Antes de Usar
-------------

- Renomear config.xml.template para config.xml
- Editar configurações de envio de e-mail em config.xml

Requisitos
----------

- Python 2.7
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
registros no intervalo especificado entre *-s* e *-e*. (ex: main.py -s 
01/01/2014 -e 01/02/2014) Nenhum e-mail será
enviado. Apenas o log será atualizado.

Configuração
------------
Dentro do arquivo *config.xml* deve constar

- **User**: usuário da conta de e-mail utilizada para postar resultados;
- **Password**: senha da conta de e-mail utilizada para postar resultados;
- **From**: e-mail remetente;
- **Subject**: assunto do e-mail de resultados;
- **ServerAddress**: endereço do servidor SMTP utilizado para enviar e-mails;
- **ServerPort**: porta do servidor SMTP utilizado para enviar e-mails;
- **To**: lista de destinatários. Cas um dentro de seu respectivo **Email**;
- **Header**: cabeçalho do e-mail de resultados;
- **Footer**: rodapé do e-mail de resultados;
- **BaseDate**: especifica data de parada da ferramenta no caso da primeira
execução;
- **Proxy**: endereço do proxy não autenticado da rede. Deixar em branco caso
não haja proxy;
- **LogName**: nome do arquivo de log local.;
- **LogMode**: determina se o arquivo de log deve ser atualizado (*Append*) ou 
sobrescrito (*Overwrite*) após cada execução;

Desenvolvedores
---------------

A interface básica para busca no diário livre já existe. Para implementar uma 
nova busca é necessário herdar de *DlSearch* para incluir as opções de busca, de
*GenericParser* para incluir as expressões regulares que filtrarão os resultados
e herdar de  *ResponseProcessor*, implementando um método *Persist* (que 
receberá como parâmetro os grupos de interesse determinados pela expressão 
regular em *GenericParser* e deve ser responsável pela saída de dados desejada) e 
*ProcessEnd* caso necessário.
