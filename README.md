ProdamLab - Nomeação de Chefes de Gabinete
==========================================

Busca Nomeações de Chefes de Gabinetes das secretarias do município de São Paulo
 no [DiárioLivre](http://devcolab.each.usp.br/do/).
Faz uma busca completa na primeira vez e apenas busca informações novas nas 
execuções subsequentes

Antes de Usar
-------------

- Renomear mailer_config.xml.template para mailer.config.xml
- Editar configurações de envio de e-mail em mailer_config.xml

Requisitos
----------
- Python 2.7
- Conta de e-mail válida para envio de e-mails.

Desenvolvedores
---------------
A interface básica para busca no diário livre já existe. Para implementar uma 
nova busca é necessário herdar de *DlSearch* para incluir as opções de busca, de
*GenericParser* para incluir as expressões regulares que filtrarão os resultados
e herdar de  *ResponseProcessor*, implementando um método *Persist* (que 
receberá como parâmetro os grupos de interesse determinados pela expressão regular em 
*GenericParser* e deve ser responsável pela saída de dados desejada) e 
*ProcessEnd* caso necessário.
