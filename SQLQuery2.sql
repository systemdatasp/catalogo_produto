/* Itens Novos *
insert into catalogo.dbo.classificacao
    ( 
	[status],
	[data_cadastro],
	[pedido],
	[item],
	[codigo_produto],
	[codigo_ncm],
	[indice_ncm],
	[ncm_mac],
	[descricao_cliente],
	[descricao_tecnica],
	[usuario],
	[data_classificacao],
	[situacao],
	[cliente],
	[modalidade],
	[nrochamado],
	[dt_solucao_chamado],
	[codigo_portal],
	cnpj_raiz,
	tipo_pedido,
	data_necessidade
) 
select 0,
           getdate() as dtcadastro,
		   a.pedido,
		   a.item,
		   a.codigo_produto,
		   a.codigo_ncm,
		   null as indicencm,
		   a.ncm_outsourcing,
		   a.nome,
		   null,
		   null as usuario,
		   null as dtclassificacao,
		   1,
		   1,
		   null,
		   null,
		   null,
		   null,
           substring(centro.cnpj,1,10),
		   c.tipo_pedido,
		   b.leadtime_fabrica,
          isnull((c.qtde * preco_unitario),0) as Valor
from catalogo.dbo.classificacao xx
left join planilhas_clientes.dbo.conferencia_ncm a on a.pedido = xx.pedido and xx.item = a.item
left join planilhas_clientes.dbo.produtos_liberados b on b.pedido = a.pedido and b.item = a.item
left join planilhas_clientes.dbo.produtos c on c.pedido = a.pedido and c.item = a.item
left join planilhas_clientes.dbo.processos d on d.pedido = a.pedido
left join planilhas_clientes.dbo.centro_custo centro on centro.codigo_mac  = d.origem_requisitante
where a.cadastrado = 'N'
and b.data_aprovacao is null 

insert into catalogo.dbo.classificacao
    ( 
	[status],
	[data_cadastro],
	[pedido],
	[item],
	[codigo_produto],
	[codigo_ncm],
	[indice_ncm],
	[ncm_mac],
	[descricao_cliente],
	[descricao_tecnica],
	[usuario],
	[data_classificacao],
	[situacao],
	[cliente],
	[modalidade],
	[nrochamado],
	[dt_solucao_chamado],
	[codigo_portal],
	cnpj_raiz,
	tipo_pedido,
	data_necessidade,
	valor
) 
select 
          3,
           getdate() as dtcadastro,
		   a.pedido,
		   a.item,
		   a.codigo_produto,
		   c.codigo_nbm,
		   null as indicencm,
		   a.codigo_ncm,
		   a.nome,
		   a.observacao,
		   null as usuario,
		   null as dtclassificacao,
		   1,
		   1,
		   null,
		   null,
		   null,
		   null,
           substring(e.cnpj,1,10),
		   c.tipo_pedido,
		   b.leadtime_fabrica,
		   c.valor_total
from planilhas_clientes.dbo.conferencia_ncm a
left join planilhas_clientes.dbo.produtos_liberados b on b.pedido = a.pedido and b.item = a.item
left join planilhas_clientes.dbo.produtos c on c.pedido = a.pedido and c.item = a.item
left join planilhas_clientes.dbo.processos d on d.pedido = a.pedido and c.item = a.item
left join planilhas_clientes.dbo.centro_custo e on e.codigo_mac = d.origem_requisitante
where b.data_aprovacao is null 


update catalogo.dbo.classificacao set situacao = 2 
where id in ( 1,552)
select * from catalogo.dbo.exportadores
insert into catalogo.dbo.exportadores 
(data_cadastro,
cliente,
codigo_cliente,
endereco,
bairro,
cidade,
cep,
pais,
email,
usuario,
exportador,
subdivisao,
cnpj_portal,
situacao_portal,
codigo_tin,
codigo_portal,
versao)
select null,
          1,
		  codigo_cliente,
		  endereco,
		  bairro,
		  cidade,
		  cep,
		  'AR',
		  null,
		  null,
		  nome,
          null,
          null,
		  null,
		  null,
		  null
from planilhas_clientes.dbo.fornecedores
where nome like '%FUND%'

select distinct substring(cnpj,1,10)
from planilhas_clientes.dbo.centro_custo

create table catalogo.dbo.emails
( id int identity(1,1) primary key clustered,
  nome varchar(200),
  usuario varchar(20),
  email varchar(100),
  alter table catalogo.dbo.emails add client smallint
)






insert into catalogo.dbo.emails values('SILVIO LUIS MARTINS DE CAMPOS','SILLVIO','')
insert into catalogo.dbo.emails values('MARCO ANTONIO DA SILVA','MARTONIO','')
insert into catalogo.dbo.emails values('DIEGO DE OLIVEIRA DE MEDEIROS','MDIEGO','DIEGO.MEDEIROS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('VALMIR CAMPOS','VCAMPOS','')
insert into catalogo.dbo.emails values('JORGE THOMAZ DA SILVA','THOMAZ','THOMAZ.SILVA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('FLAVIO JOSE PEREIRA DA CRUZ','FLAVIOC','FLAVIO.CRUZ@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCELO MARQUES FELIPE','CELO','')
insert into catalogo.dbo.emails values('WALLACE RAMOS DAS GRACAS','WALLACEG','WALLACE.GRACAS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('FABIANO BATISTA VILELA','FABVIL','FABIANO.VILELA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('EVERTON LEAL LOPES','ELEAL','EVERTON.LOPES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('VITOR SOUZA DE PAULA','VITORP','')
insert into catalogo.dbo.emails values('WILLIAM DA COSTA SILVA','WILLIAMD','WILLIAM.SILVA4@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ANDRE MATTOS DE ARAUJO','AMATTOS','ANDRE.ARAUJO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('PAULO SERGIO SANTOS DA CONCEICAO','PAULOSC','PAULO.CONCEICAO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GEOVANI FURINI','GFURINI','GEOVANI.FURINI@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCOS RODOLFO SILVERIO','MRODOLFO','MARCOS.SILVERIO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('CARLOS ALEXANDRE KLEIN','CKLEIN','CARLOS.KLEIN@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('THIAGO NORIO NAKATA','THIAGON','THIAGO.NAKATA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LUIS HENRIQUE ESCH BACH','LEBACH','LUIS.BACH@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARIO SERGIO VIEIRA DE CARVALHO','MSVIEIRA','MARIO.CARVALHO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GEISON DA SILVA CAMARA','GEISON','GEISON.CAMARA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('FABIO KAZUHIRO MURAKAMI','FABIOKM','FABIO.MURAKAMI@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('SIDNEY MAGALHAES DE BRITO','SBRITO','SIDNEY.BRITO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JOSE TOSHIO KINOSHITA JUNIOR','TOSHIO','JOSE.KINOSHITA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('IVANILDO CASEMIRO DE OLIVEIRA','IVANILC','IVANILDO.OLIVEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DANILO CARVALHO DA ROCHA','DANNILO','DANILO.ROCHA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JORGE RODRIGUES DE OLIVEIRA JUNIOR','JRJUNIOR','')
insert into catalogo.dbo.emails values('MARCIO DA SILVA SIMANKE','MARCIOSI','MARCIO.SIMANKE@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCIO GERALDO PEREIRA','MARCIOGR','MARCIO.PEREIRA1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RICARDO AQUINO FERREIRA DE FREITAS','RAFREI','RICARDO.FREITAS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ITAMIR CARVALHO OLIVEIRA JUNIOR','ITAMIRCO','ITAMIR.OLIVEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('PAULINO CARDOZO JUNIOR','JUNIORPC','PAULINO.CARDOZO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('VINICIUS SANTOS RODRIGUES','LINK','')
insert into catalogo.dbo.emails values('THIAGO RABELO BRAGA','TIAGORB','THIAGO.BRAGA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MAURICIO LOPES MORAES','MAULP','MAURICIO.MORAES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RAFAEL RODRIGUES DA ROSA','RAFRAEL','RAFAEL.ROSA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DANIEL HERIBERTO DA SILVA','DAHESI','DANIEL.SILVA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JEFERSON PENA DE CARVALHO','JEFPENA','JEFERSON.CARVALHO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ALOIZIO CESAR GONZAGA','AGONZAGA','')
insert into catalogo.dbo.emails values('FABIANA GISELIA DO NASCIMENTO','GISELIAN','')
insert into catalogo.dbo.emails values('JOHN DEIVID DE OLIVEIRA','JDEIVID','JOHN.OLIVEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('IVAN DOS SANTOS TEIXEIRA','IVANDS','IVAN.TEIXEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RENATO GABRIEL DOS SANTOS','RENATOG','RENATO.SANTOS1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARIO HENRIQUE LEONARDO SARTORELLI','MHLS','MARIO.SARTORELLI@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DIOGO PIRES DE OLIVEIRA','DIOGOPO','DIOGO.OLIVEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('CINTIA DA CONCEICAO LEAO','CLEAO','CINTIA.LEAO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RODRIGO DOS SANTOS','SANTOSR','RODRIGO.SANTOS3@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('WANDERSON MATOSINHO DE PAULA','WKWN','WANDERSON.PAULA201@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LUIZ ANDRE PIRES','LAPANDRE','LUIZ.PIRES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JOSIANE GOMES SOUZA','JOSIANEG','JOSIANE.SOUZA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JOSIMAR INACIO DE OLIVEIRA','JINACIO','JOSIMAR.OLIVEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('SAMUEL LAGE VIANNA','SAMUELLV','')
insert into catalogo.dbo.emails values('JOAO VICTOR SILVA NASCIMENTO','JVSN','JOAO.NASCIMENTO1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('EDMO RIBEIRO DOS SANTOS','EDMORS','EDMO.SANTOS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('REGINALDO APARECIDO MARTINS','REGMARTI','REGINALDO.MARTINS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DAVID DE FRANCA SOARES','DFSOARES','DAVID.SOARES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RONICLEI FRANCISCO CRISPIM','RFCT','RONICLEI.CRISPIM@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MAURICIO MACHADO PEREIRA','MMMP','MAURICIO.PEREIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JOSE ELISIO COELHO','ELISIO','JOSE.COELHO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GERALDO FERREIRA DA SILVA JUNIOR','GERALDO1','')
insert into catalogo.dbo.emails values('RUBENS ALVES CORDEIRO JUNIOR','MJDRM','RUBENS.CORDEIRO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ANTONIO HENRIQUE NOGUEIRA','TOMH','ANTONIO.NOGUEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('EMERSON SOUZA FERREIRA','EMERSONF','EMERSON.FERREIRA201@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DIEGO DA SILVA NASCIMENTO','DIEGOSN','DIEGO.NASCIMENTO1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('HERMES KOITI DE MORAIS','KMORAIS','')
insert into catalogo.dbo.emails values('MOACIR PAULO MEDEIROS DA SILVA','FORCA','MOACIR.SILVA1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('EDUARDO LOPES DE OLIVEIRA','EDULO','EDUARDO.OLIVEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MAURO BAPTISTA DA SILVA','MAUROPAV','MAURO.SILVA7@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RICARDO OLIVEIRA DA SILVA','RICKSILV','RICARDO.SILVA4@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('HELTON ROMULO NASCIMENTO DA CONCEICAO','HELTONRN','')
insert into catalogo.dbo.emails values('DIEGO SANTANA DE MEDEIROS','DIEGOSAN','DIEGO.MEDEIROS1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ALAN DOUGLAS SILVA E SOUZA','ALANDOUG','')
insert into catalogo.dbo.emails values('BRUNO DA SILVEIRA AZEVEDO','BRUNOSP','BRUNO.AZEVEDO2@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('FABIANO DE SOUSA ROCHA','ROCHA10','FABIANO.ROCHA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GUILHERME SILVA SOUZA','GSSCAM','GUILHERME.SOUZA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('EDUARDO COSTA RODRIGUES','ECRODRIG','EDUARDO.RODRIGUES2@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('KLENER FERNANDES MATOZINHOS','KLENER','KLENER.MATOZINHOS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('EMILIO APARECIDO DIAS','EMIDIAS','')
insert into catalogo.dbo.emails values('JULIANE CAROLINE CAMARA DAMASO','JCCD','JULIANE.DAMASO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('IRVING NOBREGA SANTOS','IRVING','IRVING.SANTOS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ESDRAS DA SILVA EVANGELISTA','MIGESD','')
insert into catalogo.dbo.emails values('SAMUEL ALVARO MENDONCA DE SOUZA','SAMUKA','SAMUEL.SOUZA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('BRUNO SERGIO PEREIRA DE MORAES','BRUNOSPM','')
insert into catalogo.dbo.emails values('WAGNER GERALDO PAULA MACIEL','WGPM','')
insert into catalogo.dbo.emails values('WILLIAM AROLDO HONORIO','WIL1985','WIL1985@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('SAMUEL ISIDORO CEZARINO','SISIDORO','SAMUEL.CEZARINO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('THIAGO GILMAR DE LIMA SILVA','THIAGOGL','')
insert into catalogo.dbo.emails values('AIRTON EUSTAQUIO DAMIAO JUNIOR','ADJUNIOR','')
insert into catalogo.dbo.emails values('ALDO FERREIRA MOTA','ALDOMOTA','ALDO.MOTA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DANILO FIGUEIRA FERREIRA','DFRRE','DANILO.FERREIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DANILO MACHADO DA FONSECA','DANILOMF','DANILO.FONSECA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ALFREDO MACHADO JUNIOR','JUNIOR','ALFREDO.MACHADO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LEANDRO RIBEIRO DE ANDRADE','LRDA','LEANDRO.ANDRADE@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ALEXSSANDRO RODRIGUES DOS SANTOS','ALEX01','')
insert into catalogo.dbo.emails values('ROBERSON DE SOUZA LEMOS DAS FLORES','RSLEMOS','ROBERSON.FLORES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('BRUNO FRANCISCO BELTRAO DE ALBUQUERQUE','BELTRAO','')
insert into catalogo.dbo.emails values('JONATHAN ANDRE EVANGELISTA SILVA','JANDRE','')
insert into catalogo.dbo.emails values('FELIPE DE OLIVEIRA DIAS','FDIAS','FELIPE.DIAS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DOUGLAS AKIRA REIS KUSANO','DKUSANO','DOUGLAS.KUSANO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('VILMAR DAS GRACAS SANTOS GOMES','VGRACAS','VILMAR.GOMES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GUILHERME HENRIQUE DE OLIVEIRA','GHENRI01','GUILHERME.OLIVEIRA201@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('FERNANDA CRISTINA DE PAULA','FPAULA01','FERNANDA.PAULA1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('WAGNER DIEGO ROSA SOARES','WDROSA','WAGNER.SOARES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GIOVANNI SILVANO FERREIRA','GSF2612','')
insert into catalogo.dbo.emails values('ALVARO AUGUSTO DA SILVA SOUZA','ALVAROSS','')
insert into catalogo.dbo.emails values('DANILO RYAN DO NASCIMENTO CRUZ','CRUZ','DANILO.CRUZ1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('HEBERT KLEMICHAK KAMROYAN','KAMROYAN','')
insert into catalogo.dbo.emails values('MATHEUS MARCOS LOPES ALVES','LOPES25','')
insert into catalogo.dbo.emails values('MAYCON GONCALVES FERREIRA','MGF01','MAYCON.FERREIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('BRUNO CARDOSO ALCANTARA','BCARDO01','BRUNO.ALCANTARA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LUIS ANDRE RAMALHO ALVES','LANDRE01','LUIS.ALVES1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JEAN LUIZ VILAS BOAS','JEANVB','')
insert into catalogo.dbo.emails values('IVAIR SOARES VIEIRA','GIGUIGA','IVAIR.VIEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('EMERSON CARLOS DA ROCHA','MERCIM','EMERSON.ROCHA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('BRUNO ALVARES','BALVARES','BRUNO.ALVARES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('WANDERSON DE PAULA LIMA','TALISSAA','WANDERSON.LIMA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RODRIGO EIJI AMANO','REAMANO','RODRIGO.AMANO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('CLAYTON LELIS DE RESENDE','DJSUMER','')
insert into catalogo.dbo.emails values('LAZARO COELHO PEREIRA','LAZAROCP','')
insert into catalogo.dbo.emails values('EDUARDO RODRIGUES VIEIRA','REDUARDO','EDUARDO.VIEIRA200@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARLUCIO GERALDO SIMAO','TEODORO','MARLUCIO.SIMAO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DAVIDSON FABIANO RODRIGUES','DFRAS','DAVIDSON.RODRIGUES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('CHARLES GONCALVES RIBEIRO','CCHARLES','CHARLES.RIBEIRO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LEONARDO SOARES NOGUEIRA','LEOSN','LEONARDO.NOGUEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GILSON RODRIGUES DE CARVALHO BRAGA','GALACO','GILSON.BRAGA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCOS TORRES DA FONSECA','CENOURA','MARCOS.FONSECA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCIO RODRIGUES','RODRIGM','MARCIO.RODRIGUES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ADENIR MENDES','ADEMEND','ADENIR.MENDES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('THOMAZ JEREMIAS ALVES DA CRUZ','TCRUZ','THOMAZ.CRUZ@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('VALDIR DO AMARAL','VALDIRAM','')
insert into catalogo.dbo.emails values('JAIRO GONCALVES DUQUE','JGDUQUE','JAIRO.DUQUE@GERDAUSUMMIT.COM')
insert into catalogo.dbo.emails values('LUIZ FERNANDO BERNARDES','LFBERNAR','LUIZ.BERNARDES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JOEL MOREIRA DOS SANTOS PINTO','JOELM','')
insert into catalogo.dbo.emails values('LINCOLN JORGE DE ALMEIDA SOUZA','JLINCOLN','LINCOLN.SOUZA@GERDAUSUMMIT.COM')
insert into catalogo.dbo.emails values('ALEXANDRE BASILIO HENRIQUES PAIVA','AHENRIQU','ALEXANDRE.PAIVA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('SERGIO MENDES DE CARVALHO','SMCARVAL','SERGIO.CARVALHO@GERDAUSUMMIT.COM')
insert into catalogo.dbo.emails values('THALITA DE CASTRO CASTILHO','TCASTILH','')
insert into catalogo.dbo.emails values('RENATO LUCAS APARECIDO DA SILVA','RENATLAS','')
insert into catalogo.dbo.emails values('MARCIO FOGACA DE LIMA','MARCIOFL','MARCIO.LIMA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MICHEL DONIZETI CARDOSO','CARDOSMD','')
insert into catalogo.dbo.emails values('FERNANDO ALVES DE OLIVEIRA','FALVES','FERNANDO.OLIVEIRA2@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('PHAGNER PHILIPE DE OLIVEIRA TEIXEIRA','PPHILIPE','PHAGNER.TEIXEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DENILSON SILVA DA SILVA','DENISCI','')
insert into catalogo.dbo.emails values('JOAO LUCAS VIEIRA DA SILVA','JLUCAS03','JOAO.SILVA1501@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('CAMILA DANIELE FERNANDES','CDANIELE','CAMILA.FERNANDES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('PEDRO REBEQUI DA COSTA SOUZA MENDES','PMENDES1','')
insert into catalogo.dbo.emails values('LUIS GUSTAVO SAGLIOCCO RAPHAEL','SAGLIOCC','')
insert into catalogo.dbo.emails values('RENAN LUIZ DE OLIVEIRA','ROLIVEI2','RENAN.OLIVEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GIAN DOS SANTOS OLIVEIRA MENDONCA','GMENDON1','')
insert into catalogo.dbo.emails values('HENRIQUE BARROS VIEIRA FERNANDES','HFERNAN3','')
insert into catalogo.dbo.emails values('LARISSA FATIMA DA SILVA FLORINDO','LFLORIND','')
insert into catalogo.dbo.emails values('HEBERT KLEMICHAK KAMROYAN','KAMROYAN','HEBERT.KAMROYAN@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ANDREY SCHMIDT DOS SANTOS','ASANTO27','')
insert into catalogo.dbo.emails values('DENILSON SILVA DA SILVA','DENISCI','DENILSON.SILVA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCO TULIO CARMOZINE PRADO','MPRADO1','MARCO.PRADO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LUIS GUSTAVO SAGLIOCCO RAPHAEL','SAGLIOCC','')
insert into catalogo.dbo.emails values('KLEBER ALVES DE LIMA','KLIMA1','')
insert into catalogo.dbo.emails values('ROMULO FERNANDES DA SILVA','RSILVA54','')
insert into catalogo.dbo.emails values('MATHEUS MARCOS LOPES ALVES','LOPES25','MATHEUS.LOPES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LEANDRO REGIS DE PAULA','LPAULA1','LEANDRO.PAULA301@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ANDERSON RODRIGO MACHADO DOS SANTOS','ASANTO40','ANDERSON.SANTOS801@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCELO LUDWIG ARNOLD','MARNOLD1','')
insert into catalogo.dbo.emails values('IGOR MARCOLINO DA SILVA','ISILVA7','')
insert into catalogo.dbo.emails values('ROMULO FERNANDES DA SILVA','RSILVA54','')
insert into catalogo.dbo.emails values('BRUNO ALESSANDRO DOS SANTOS','BSANTOS8','')
insert into catalogo.dbo.emails values('GIAN DOS SANTOS OLIVEIRA MENDONCA','GMENDON1','GIAN.MENDONCA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LARISSA FATIMA DA SILVA FLORINDO','LFLORIND','LARISSA.FLORINDO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCELO LUDWIG ARNOLD','MARNOLD1','MARCELO.ARNOLD@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ANDREY SCHMIDT DOS SANTOS','ASANTO27','ANDREY.SANTOS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MICHAEL DOUGLAS BRIGAGAO PENNAFIRME','MPENNAFI','')
insert into catalogo.dbo.emails values('MARCELO TEIXEIRA AGUIAR','MAGUIAR1','')
insert into catalogo.dbo.emails values('IGOR MARCOLINO DA SILVA','ISILVA7','IGOR.SILVA1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LILIAN STEPHANIE DIAS DO PORTO','LPORTO1','')
insert into catalogo.dbo.emails values('LEANDRO MARQUES PAIM','LPAIM','')
insert into catalogo.dbo.emails values('WAGNER FORTUNATO LASNOU DE OLIVEIRA','WOLIVEI7','')
insert into catalogo.dbo.emails values('LIGIA DOS SANTOS DE OLIVEIRA','LOLIVE23','')
insert into catalogo.dbo.emails values('LILIAN STEPHANIE DIAS DO PORTO','LPORTO1','LILIAN.PORTO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('PAULO RICARDO CROGITE JUNIOR','PCROGITE','')
insert into catalogo.dbo.emails values('VANESSA DO CARMO MARTINS','VMARTIN2','')
insert into catalogo.dbo.emails values('MARIANE CASTELO BRANCO BAPTISTA','MBRANCO','')
insert into catalogo.dbo.emails values('IGOR CORDEIRO DOS PASSOS SILVA','ISILVA23','')
insert into catalogo.dbo.emails values('HENRIQUE DE PAULA GONZAGA','HGONZAGA','')
insert into catalogo.dbo.emails values('WAGNER FORTUNATO LASNOU DE OLIVEIRA','WOLIVEI7','WAGNER.OLIVEIRA3@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JORGE RODRIGUES DE OLIVEIRA JUNIOR','JRJUNIOR','JORGE.OLIVEIRA2@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LEANDRO MARQUES PAIM','LPAIM','LEANDRO.PAIM@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('THIAGO GILMAR DE LIMA SILVA','THIAGOGL','THIAGO.SILVA11@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MICHAEL DOUGLAS BRIGAGAO PENNAFIRME','MPENNAFI','MICHAEL.PENNAFIRME@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCOS VINICIUS SALGADO BARBOSA','MBARBOS9','')
insert into catalogo.dbo.emails values('HERMES KOITI DE MORAIS','KMORAIS','')
insert into catalogo.dbo.emails values('PEDRO REBEQUI DA COSTA SOUZA MENDES','PMENDES1','')
insert into catalogo.dbo.emails values('ALVARO AUGUSTO DA SILVA SOUZA','ALVAROSS','ALVARO.SOUZA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ALAN DOUGLAS SILVA E SOUZA','ALANDOUG','ALAN.SOUZA@GERDAUSUMMIT.COM')
insert into catalogo.dbo.emails values('GABRIEL DOMENICO RODRIGUES FONSECA DA SI','GSILVA84','')
insert into catalogo.dbo.emails values('GABRIEL CARMONA DE OLIVEIRA CAMARGO','GCAMARG3','')
insert into catalogo.dbo.emails values('PAULO RICARDO CROGITE JUNIOR','PCROGITE','PAULO.CROGITE@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('BRUNO ALESSANDRO DOS SANTOS','BSANTOS8','BRUNO.SANTOS6@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('KARINA PIRES DE CASTRO SOUZA','KSOUZA7','')
insert into catalogo.dbo.emails values('JOAO VITOR MORAES FERREIRA','JFERRE23','')
insert into catalogo.dbo.emails values('SIMEONY OLIVEIRA ZUFFO','SZUFFO','')
insert into catalogo.dbo.emails values('JOAO VICTOR GOMES LIMA','JLIMA16','')
insert into catalogo.dbo.emails values('LUIS GUSTAVO SAGLIOCCO RAPHAEL','SAGLIOCC','LUIS.SAGLIOCCO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('PAULO BRANDAO SANTOS','PSANTO12','PAULO.SANTOS13@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LUIS GUSTAVO COELHO','LCOELHO8','')
insert into catalogo.dbo.emails values('ELISA FRANCISCO DE SOUSA','ESOUSA4','')
insert into catalogo.dbo.emails values('DIRLENE SANTOS CRUZ','DCRUZ5','')
insert into catalogo.dbo.emails values('BEATRIZ ALVES COSMO','BCOSMO1','')
insert into catalogo.dbo.emails values('KLEBER ALVES DE LIMA','KLIMA1','KLEBER.LIMA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('HELTON ROMULO NASCIMENTO DA CONCEICAO','HELTONRN','HELTON.CONCEICAO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('HUGO MURATA','HMURATA','')
insert into catalogo.dbo.emails values('HENRIQUE LEONAN CAVALI ALMEIDA','HALMEID5','')
insert into catalogo.dbo.emails values('VITOR SOUZA DE PAULA','VITORP','VITOR.PAULA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GABRIEL CARMONA DE OLIVEIRA CAMARGO','GCAMARG3','GABRIEL.CAMARGO1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DIVANOR JESUS LIMA DOS SANTOS','DSANTO34','DIVANOR.SANTOS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCO TULIO CARMOZINE PRADO','MPRADO1','MARCO.PRADO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DANIEL JOSE MARQUES RODRIGUES','DRODRI16','DANIEL.RODRIGUES5@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LIGIA DOS SANTOS DE OLIVEIRA','LOLIVE23','')
insert into catalogo.dbo.emails values('HENRIQUE DE PAULA GONZAGA','HGONZAGA','HENRIQUE.GONZAGA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('VANESSA DO CARMO MARTINS','VMARTIN2','VANESSA.MARTINS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('IGOR CORDEIRO DOS PASSOS SILVA','ISILVA23','IGOR.SILVA8@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('SIMEONY OLIVEIRA ZUFFO','SZUFFO','')
insert into catalogo.dbo.emails values('JOAO VICTOR GOMES LIMA','JLIMA16','JOAO.LIMA1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('KARINA PIRES DE CASTRO SOUZA','KSOUZA7','KARINA.SOUZA1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JEAN MICHEL PORFIRIO DA COSTA','JCOSTA23','JEAN.COSTA1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('THUANY CAMILA DA PAIXAO VIANA','TVIANA3','THUANY.VIANA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LEONARDO DE SIQUEIRA NOGUEIRA','LNOGUEI3','')
insert into catalogo.dbo.emails values('MARIANA SANTOS BRITO','MBRITO2','')
insert into catalogo.dbo.emails values('SAMUEL LAGE VIANNA','SAMUELLV','SAMUEL.VIANNA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('VALDIR DO AMARAL','VALDIRAM','VALDIR.AMARAL@GERDAUSUMMIT.COM')
insert into catalogo.dbo.emails values('HENRIQUE LEONAN CAVALI ALMEIDA','HALMEID5','')
insert into catalogo.dbo.emails values('LEONARDO DE SIQUEIRA NOGUEIRA','LNOGUEI3','LEONARDO.NOGUEIRA1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('CESAR ALANDER NORBERTO','CNORBER1','CESAR.NORBERTO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GABRIEL DOMENICO RODRIGUES FONSECA DA SI','GSILVA84','')
insert into catalogo.dbo.emails values('VANDER LUCIO PINTO','VPINTO4','')
insert into catalogo.dbo.emails values('LUIS GUSTAVO COELHO','LCOELHO8','LUIS.COELHO1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('AIRTON EUSTAQUIO DAMIAO JUNIOR','ADJUNIOR','AIRTON.DAMIAO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DIRLENE SANTOS CRUZ','DCRUZ5','DIRLENE.CRUZ@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GIOVANE CRISTIANO VITORIANO DE AQUINO','GAQUINO2','')
insert into catalogo.dbo.emails values('DANIEL SCHMIDT DE ARRUDA','DARRUDA2','DANIEL.ARRUDA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RAFAEL HENRIQUES RODRIGUES','RRODRI32','RAFAEL.RODRIGUES2@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LEANDRO RIOS DE ALMEIDA','LALMEI15','')
insert into catalogo.dbo.emails values('MARIA RITA PIRES DA SILVA','MSILV171','')
insert into catalogo.dbo.emails values('JOAO VITOR MORAES FERREIRA','JFERRE23','JOAO.FERREIRA4@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LARISSA MARTINS ROSA','LROSA9','')
insert into catalogo.dbo.emails values('BRUNO SERGIO PEREIRA DE MORAES','BRUNOSPM','BRUNO.MORAES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GABRIELLY MARTINS BARRETO','GBARRET2','')
insert into catalogo.dbo.emails values('MICHELE ESTELA DIAS PEREIRA','MPEREI22','')
insert into catalogo.dbo.emails values('PEDRO MEDEIROS MELO','PMELO5','PEDRO.MELO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('BEATRIZ ALVES COSMO','BCOSMO1','BEATRIZ.COSMO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ALEXANDRE CARLOS DOMINGUES VASCONCELOS','AVASCON3','ALEXANDRE.VASCONCELOS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ESDRAS DA SILVA EVANGELISTA','MIGESD','ESDRAS.EVANGELISTA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ROGERIO DE ARAUJO MOREIRA','RMOREIR8','ROGERIO.MOREIRA3@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('FABRICIO FRANKLIN ROCHA','FROCHA8','FABRICIO.ROCHA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ELISA FRANCISCO DE SOUSA','ESOUSA4','ELISA.SOUSA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JOSIMAR RESENDE CORREA','JCORREA3','JOSIMAR.CORREA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GIOVANE CRISTIANO VITORIANO DE AQUINO','GAQUINO2','GIOVANE.AQUINO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('VITORIA IMACULADA RODRIGUES CAMPOS','VCAMPOS','VITORIA.CAMPOS1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GABRIELLY MARTINS BARRETO','GBARRET2','GABRIELLY.BARRETO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARIANA SANTOS BRITO','MBRITO2','MARIANA.BRITO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('DAYANE KAROLINA BARRO LEAL','DLEAL2','')
insert into catalogo.dbo.emails values('DANIELE DIAS ARAUJO','DARAUJ18','DANIELE.ARAUJO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('EDUARDA SOARES DE SALES AMORIM','EAMORIM4','EDUARDA.AMORIM@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('SOFIA NOGUEIRA AMORIM','SAMORIM2','')
insert into catalogo.dbo.emails values('CELSO DA SILVA ALBUQUERQUE JUNIOR','CJUNIO13','')
insert into catalogo.dbo.emails values('NATALIA BAPTISTA BARTSCH','NBARTSCH','')
insert into catalogo.dbo.emails values('THIAGO HENRIQUE LIMA PEREIRA DE BARROS','TBARROS4','')
insert into catalogo.dbo.emails values('MICHELLE ESTELA DIAS PEREIRA','MPEREI22','MICHELE.PEREIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('VANESSA FISCHER DA SILVEIRA FISCHER','VFISCHER','VANESSA.FISCHER@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RICARDO MONTEIRO LARA ARAUJO','RARAUJ13','')
insert into catalogo.dbo.emails values('PEDRO LUAN NEVES','PNEVES2','PEDRO.NEVES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LEANDRO DE SOUZA SILVA','LSILV200','LEANDRO.SILVA21@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GERALDO FERREIRA DA SILVA JUNIOR','GERALDO1','GERALDO.SILVA2@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RAFAEL BAPTISTA FROES','RFROES','')
insert into catalogo.dbo.emails values('DENILSON DA CONCEICAO FEIJO JUNIOR','DJUNIOR4','DENILSON.FEIJO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MAIRA LUCIA MAIA RODRIGUES','MRODRI38','')
insert into catalogo.dbo.emails values('MARCOS ROBERTO BELICIO TORRES','MTORRES5','MARCOS.TORRES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('PEDRO REBEQUI DA COSTA SOUZA MENDES','PMENDES1','PEDRO.MENDES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('SAMARA HELEN DA MATTA BARBOSA','SBARBOS6','SAMARA.BARBOSA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LUCAS LEONARDO PEREIRA LIMA','LLIMA27','LUCAS.LIMA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('HENRIQUE BARROS VIEIRA FERNANDES','HFERNAN3','HENRIQUE.FERNANDES200@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LUCAS VINICIUS DA SILVA FONSECA','LFONSEC9','LUCAS.FONSECA2@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCELO TEIXEIRA AGUIAR','MAGUIAR1','')
insert into catalogo.dbo.emails values('CARLOS ALEXANDRE GONCALVES DE MOURA','CMOURA4','')
insert into catalogo.dbo.emails values('GABRIEL DELGADO PAULO','GPAULO1','')
insert into catalogo.dbo.emails values('RAYANE ISMAEL DA SILVA ROSA','RROSA11','')
insert into catalogo.dbo.emails values('PEDRO HENRIQUE MOREIRA SOARES SILVEIRA','PSILVEI3','')
insert into catalogo.dbo.emails values('NADIA NETO MOURA','NMOURA2','')
insert into catalogo.dbo.emails values('MARIANE CASTELO BRANCO BAPTISTA','MBRANCO','MARIANE.BRANCO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MANOEL JOSE PEDROSA FILHO','MFILHO8','')
insert into catalogo.dbo.emails values('JOSIANE PIRES SANTOS','JSANT152','JOSIANE.SANTOS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARIANA APARECIDA MAXIMO','MMAXIMO','MARIANA.MAXIMO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARIA GABRIELA VENTURA DA SILVA','MSILV252','')
insert into catalogo.dbo.emails values('LARISSA MARTINS ROSA','LROSA9','')
insert into catalogo.dbo.emails values('LAIS FIGUEIREDO VIEIRA','LVIEIR19','LAIS.VIEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GUILHERME CALEFANO TRINDADE DOS SANTOS','GSANTO95','')
insert into catalogo.dbo.emails values('FABIANA GISELIA DO NASCIMENTO','GISELIAN','FABIANA.NASCIMENTO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MATHEUS LUIZ LIMA DE SANTANA','MSANTAN7','')
insert into catalogo.dbo.emails values('LUCIANO CAMPANATE FERREIRA','LCFERR','LUCIANO.FERREIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JOSE STENIO BENIGNO DE MATOS','JBENIGN','JOSE.MATOS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('HUDSON CARLOS RAIMUNDO','HUDSONCR','HUDSON.RAIMUNDO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GILVAN CHAGAS DA COSTA','GILVANC','GILVAN.COSTA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RAFAEL MACIEL DE FREITAS RAMOS','RMFREIT','')
insert into catalogo.dbo.emails values('DAYANE KAROLINA BARRO LEAL','DLEAL2','DAYANE.LEAL@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('BRUNO FERNANDES BRAGUETTO','BBRAGUET','BRUNO.BRAGUETTO@GERDAUSUMMIT.COM')
insert into catalogo.dbo.emails values('RAFAEL DE MATTOS MONTEIRO','RMONTEI2','RAFAEL.MONTEIRO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LIVIA DIAS BISCARO','LBISCARO','')
insert into catalogo.dbo.emails values('DIOGO GONCALVES MIRANDA','DMIRAND5','')
insert into catalogo.dbo.emails values('MARCO ANTONIO DA COSTA','MCOSTA33','MARCO.COSTA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ANA LUIZA VIEIRA AGUILAR','AAGUILA3','')
insert into catalogo.dbo.emails values('SILAS DOS SANTOS RIBEIRO','SRIBEIR4','')
insert into catalogo.dbo.emails values('RICHARD DELLER','RDELLER','RICHARD.DELLER@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GUSTAVO DE SOUZA EHLERT','GEHLERT','GUSTAVO.EHLERT@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('REGINALDO BRAGA DE CARVALHO','RCARVA22','REGINALDO.CARVALHO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('CLAUDIA REGINA DE OLIVEIRA','COLIVE40','')
insert into catalogo.dbo.emails values('NATASHA CRISTINA MACHADO DA ROCHA','NROCHA4','NATASHA.ROCHA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ROMULO FERNANDES DA SILVA','RSILVA54','')
insert into catalogo.dbo.emails values('DIOGO MONTEIRO DO NASCIMENTO','DNASCI19','DIOGO.NASCIMENTO2@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LAZARO COELHO PEREIRA','LAZAROCP','LAZARO.PEREIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RODRIGO OBERLEY OLIVEIRA MENDES','RMENDES8','RODRIGO.MENDES2@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARIELA DA SILVA PEREIRA','MPEREI35','MARIELA.PEREIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('HUMBERTO GUIMARAES QUIOSSA','HQUIOSSA','HUMBERTO.QUIOSSA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MYLENE DE SOUZA LOUZADA','MLOUZAD1','MYLENE.LOUZADA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('SILAS DOS SANTOS RIBEIRO','SRIBEIR4','SILAS.RIBEIRO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MAIRA LUCIA MAIA RODRIGUES','MRODRI38','MAIRA.RODRIGUES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('EDUARDO SAUER FONTANA','EFONTANA','')
insert into catalogo.dbo.emails values('MATHEUS LUIZ LIMA DE SANTANA','MSANTAN7','MATHEUS.SANTANA1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ORDILEI TAVARES DE CASTRO','OCASTRO1','ORDILEI.CASTRO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('NATALIA BAPTISTA BARTSCH','NBARTSCH','NATALIA.BARTSCH@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCELO HENRIQUE DA SILVA','MSILV300','MARCELO.SILVA22@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('VIVIANE APARECIDA SIQUEIRA DO NASCIMENTO','VNASCI12','VIVIANE.NASCIMENTO1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('THAIANE ELISA DE SOUZA ALVES','TALVES14','')
insert into catalogo.dbo.emails values('FABRICIO SOARES DO NASCIMENTO','FASCIME7','')
insert into catalogo.dbo.emails values('TATHIANE TARIFFE FONTOLAM','TFONTOLA','')
insert into catalogo.dbo.emails values('FRANCISCO GONCALVES RAVISON','FRAVISON','FRANCISCO.RAVISON@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RAFAEL BAPTISTA FROES','RFROES','RAFAEL.FROES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('NADIA NETO MOURA','NMOURA2','')
insert into catalogo.dbo.emails values('THIAGO HENRIQUE LIMA PEREIRA DE BARROS','TBARROS4','')
insert into catalogo.dbo.emails values('THIAGO PEREIRA DE MEDEIROS SILVA','TSILV151','THIAGO.SILVA27@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GABRIEL DELGADO PAULO','GPAULO1','GABRIEL.PAULO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('PEDRO HENRIQUE MOREIRA SOARES SILVEIRA','PSILVEI3','PEDRO.SILVEIRA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARIA GABRIELA VENTURA DA SILVA','MSILV252','MARIA.SILVA15@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JAQUELINE DOS SANTOS SILVA BARROS','JBARROS5','JAQUELINE.BARROS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('CELSO DA SILVA ALBUQUERQUE JUNIOR','CJUNIO13','')
insert into catalogo.dbo.emails values('GABRIELA EMELLY DA SILVA CAMPOS','GCAMPOS7','')
insert into catalogo.dbo.emails values('MARIA RITA PIRES DA SILVA','MSILV171','MARIA.SILVA1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MARCELO HENRIQUE DA PAIXAO','MPAIXAO4','MARCELO.PAIXAO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('TATIANE DOS REIS PENHA MELO','TMELO9','TATIANE.MELO1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JONATAS MENDES DOS SANTOS','JSANT202','JONATAS.SANTOS1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ALEXSSANDRO RODRIGUES DOS SANTOS','ALEX01','ALEXSSANDRO.SANTOS1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('THALITA DE CASTRO CASTILHO','TCASTILH','THALITA.CASTILHO@GERDAUSUMMIT.COM')
insert into catalogo.dbo.emails values('THAISA DE OLIVEIRA REIS','TREIS5','THAISA.REIS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('RAYANE ISMAEL DA SILVA ROSA','RROSA11','RAYANE.ROSA@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('MICHAEL DA SILVA BARCELOS','MBARCEL4','MICHAEL.BARCELOS@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('ALECIO MENEZES MACIEL','AMACIEL2','ALECIO.MACIEL@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JOAO PEDRO ZIBETTI','JZIBETTI','JOAO.ZIBETTI@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LIVIA DIAS BISCARO','LBISCARO','LIVIA.BISCARO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('GUILHERME CALEFANO TRINDADE DOS SANTOS','GSANTO95','GUILHERME.SANTOS14@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('CARLOS AUGUSTO SHIGA DO CARMO','CCARMO5','')
insert into catalogo.dbo.emails values('JOHN LUCAS DA SILVA','JSILV368','JOHN.SILVA2@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('JOAO PEDRO DE FREITAS SOUZA','JSOUZ106','')
insert into catalogo.dbo.emails values('DIOGO GONCALVES MIRANDA','DMIRAND5','DIOGO.MIRANDA1@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('FABRICIO SOARES DO NASCIMENTO','FASCIME7','FABRICIO.NASCIMENTO@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('LUCAS RODRIGUES OLIVEIRA','LOLIV103','LUCAS.OLIVEIRA17@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('PETERSON DANILO DE OLIVEIRA','POLIVE49','PETERSON.OLIVEIRA@GERDAUSUMMIT.COM')
insert into catalogo.dbo.emails values('THAIANE ELISA DE SOUZA ALVES','TALVES14','THAIANE.ALVES@GERDAU.COM.BR')
insert into catalogo.dbo.emails values('CARLOS AUGUSTO SHIGA DO CARMO','CCARMO5','CARLOS.CARMO@GERDAU.COM.BR')

select * from catalogo.dbo.emails

create table catalogo.dbo.usuario
(
   id int identity(1,1) primary key clustered,
   login varchar(max),
   nome varchar(100),
   password varbinary(max),
   email varchar(100)
)
GO

 # Criando Senha Master
create master key encryption
BY PASSWORD = 'Sql*catalogo@2024!'
go

# Criando um Certificado
create certificate certificado_catalogo
ENCRYPTION BY PASSWORD = 'Sql*catalogo@2024'
WITH SUBJECT = 'Certificado Catalogo'
GO

create symmetric key chave_catalogo
with algorithm = AES_256
encryption by certificate certificado_catalogo

open symmetric key 'chave_catalogo'
decryption by certificate certificado_catalogo
declare @guid uniqueidentifier = ( select key_guid('chave_catalogo'))
insert into catalogo.dbo.usuario values ('jarcanjo','Joice Arcanjo',HASHBYTES('SHA2_256', 'cata@2025!'))
select * from catalogo.dbo.usuario
select * from catalogo.dbo.status
insert into catalogo.dbo.usuario(Username, SenhaHash)
VALUES (
    'usuario_teste', 
    HASHBYTES('SHA2_256', 'senha123')
);

select HASHBYTES('SHA2_256','cata@2025!')
from catalogo.dbo.usuario
where login = 'ealmeida' and password = HASHBYTES('SHA2_256','cata@2025!')

create 
where login = 'ealmeida' 
and password = HASHBYTES('SHA_256','cata@2025!')

select * from catalogo.dbo.status
select * from catalogo.dbo.classificacao
where status = 4

update catalogo.dbo.classificacao set status = 0 where id = 1

insert into catalogo.dbo.usuario values ('ealmeida','Erivaldo de Almeida',HASHBYTES('SHA2_256', 'cata@2025!'),'ealmeida@maclogistic.com')
insert into catalogo.dbo.usuario values ('jarcanjo','Joice Arcanjo',HASHBYTES('SHA2_256', 'cata@2025!'))
insert into catalogo.dbo.usuario values ('jarcanjo','Joice Arcanjo',HASHBYTES('SHA2_256', 'cata@2025!'))


select * from catalogo.dbo.clientes
select * from catalogo.dbo.cnpj_raiz
select * from catalogo.dbo.cnpj_raiz where cnpj = '17.227.422'
delete from catalogo.dbo.detalhes_classificacao where idclassificacao = 148
select * from catalogo.dbo.classificacao where  id = 517

create table catalogo.dbo.login_sistema
( 
   id int identity(1,1) primary key clustered,
   datalogin datetime,
   usuario varchar(20),
   alter table catalogo.dbo.login_sistema add tipo varchar(6)
) 
select * catalogo.dbo.classificacao where id = '517'
update catalogo.dbo.classificacao set cnpj_raiz = '02.634.915 07.358.761 07.359.641 07.538.761 17.227.422 24.554.306 33.611.500'
where id = 517 

 select * from catalogo.dbo.cnpj_raiz
 USE [catalogo]
CREATE TABLE [dbo].[cadatro_classificacao]
(
	id int IDENTITY(1,1) NOT NULL,
    idclassificacao int not null,
	data_classificacao [datetime] NULL,
	codigo_portal int,
	cnpj_raiz text NULL,
	constraint pk_id_classificacao primary key clustered(id),
	constraint fk_id_classificacao foreign key(idclassificacao) references catalogo.dbo.classificacao(id)
) 



  