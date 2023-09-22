entregas="""
SELECT
        scheduletype
        ,serviceLocal
        ,team
        ,teamExecution
        ,agent
        ,alternativeIdentifier
        ,dateA

        ,CASE WHEN (TO_CHAR(hourA,'HH24:MI')) IS NULL
                    THEN '00:00' else (TO_CHAR(hourA,'HH24:MI'))   
         END AS hourA

         ,executionForecastEndDate

         ,CASE WHEN (TO_CHAR(executionForecastEndTime,'HH24:MI')) IS NULL
                    THEN '00:00' else (TO_CHAR(executionForecastEndTime,'HH24:MI')) 
         END AS executionForecastEndTime
         
         ,observation
         ,situation
         ,customfield1
         ,customfield2
         ,tar_veiculo
         ,tar_embarcador
         ,STRING_AGG(listas_ctes,'/') as listas_ctes

 

FROM(   SELECT 
                'entrega'::TEXT AS scheduleType
                ,FNC_FORMATA_CNPJCPFCOD(conhecimento.destinatario) AS serviceLocal
                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque.cnpjcpfcodigoveiculo),1,10) AS team
                ,0::integer AS teamExecution
                ,FNC_FORMATA_CNPJCPFCOD(programacaoembarque.motorista) AS agent

                ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
                                                 ||'-'||programacaoembarque.diferenciadornumero
                                                 ||'-'||programacaoembarque.numero
                                                 ||'-'||FNC_FORMATA_CNPJCPFCOD(conhecimento.destinatario)
                                                 ||'-'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
                        ) AS alternativeIdentifier

                ,COALESCE(conhecimento.dtprevisaoentrega,programacaoembarque.dtprevisaosaidaviagem)::DATE AS dateA

                ,janela.inicio AS hourA

                ,COALESCE(conhecimento.dtprevisaoentrega,programacaoembarque.dtprevisaosaidaviagem)::DATE AS executionForecastEndDate
                
                ,janela.fim AS executionForecastEndTime

                ,CONCAT('Remetente:'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
                        ||' '||'Quantidade:'||programacaoembarque.quantidade
                        ||' '||'Peso:'||programacaoembarque.peso
                        ||' '||'P.E:'||programacaoembarque.grupo
                        ||'-'||programacaoembarque.empresa
                        ||'-'||programacaoembarque.diferenciadornumero
                        ||'-'||programacaoembarque.numero
                ) AS observation

                ,30::integer AS situation

                ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
                                                 ||'-'||programacaoembarque.filialdocumentoorigem
                                                 ||'-'||programacaoembarque.unidadedocumentoorigem
                                                 ||'-'||programacaoembarque.diferenciadornumerodocumentoorigem
                                                 ||'-'||programacaoembarque.seriedocumentoorigem
                                                 ||'-'||programacaoembarque.numerodocumentoorigem
                        ) AS customField1

                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10) AS customField2
                ,programacaoembarque.veiculo AS tar_veiculo
                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10) AS tar_embarcador
                ,conhecimento.chaveacessocte AS listas_ctes

        FROM programacaoembarque

    LEFT JOIN programacaoembarque_composicao
            ON programacaoembarque.grupo = programacaoembarque_composicao.grupo
            AND programacaoembarque.empresa = programacaoembarque_composicao.empresa
            AND programacaoembarque.diferenciadornumero = programacaoembarque_composicao.diferenciadornumero
            AND programacaoembarque.numero = programacaoembarque_composicao.numero
            AND programacaoembarque_composicao.tipodocumento = 6

    LEFT JOIN conhecimento
            ON programacaoembarque_composicao.grupo = conhecimento.grupo
            AND programacaoembarque_composicao.empresa = conhecimento.empresa
            AND programacaoembarque_composicao.filialdocumento = conhecimento.filial
            AND programacaoembarque_composicao.unidadedocumento = conhecimento.unidade
            AND programacaoembarque_composicao.diferenciadornumerodocumento = conhecimento.diferenciadornumero
            AND programacaoembarque_composicao.seriedocumento = conhecimento.serie
            AND programacaoembarque_composicao.numerodocumento = conhecimento.numero
            
    
    LEFT JOIN LATERAL(SELECT   codigo
                                ,max(ini) AS inicio
                                ,max(fim) AS fim 

                    
                        FROM ( SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebersegundafeira AS ini ,hrfinalcoletarrecebersegundafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                                     UNION ALL
                               SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebertercafeira AS ini ,hrfinalcoletarrecebertercafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                                     UNION ALL
                               SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarreceberquartafeira AS ini ,hrfinalcoletarreceberquartafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                                     UNION ALL
                               SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarreceberquintafeira AS ini ,hrfinalcoletarreceberquintafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                                     UNION ALL
                               SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebersextafeira AS ini ,hrfinalcoletarrecebersextafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                             ) as base
                            
                                GROUP BY codigo
                       )janela

            ON conhecimento.destinatario = janela.codigo

 WHERE programacaoembarque.numero < 1000000 
    AND programacaoembarque.unidade = 1
    AND programacaoembarque.dtemissao::date = now()::date
    AND SUBSTRING(conhecimento.destinatario,1,8) = '96662168'
    AND conhecimento.remetente = '96662168016992'

----------------------------------------  NOTA FISCAL DE SERVIÇO ---------------------------------------
UNION ALL


	SELECT 
                'entrega'::TEXT AS scheduleType
                ,FNC_FORMATA_CNPJCPFCOD(notafiscalservico_calculofrete.destinatario) AS serviceLocal
                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque.cnpjcpfcodigoveiculo),1,10) AS team
                ,0::integer AS teamExecution
                ,FNC_FORMATA_CNPJCPFCOD(programacaoembarque.motorista) AS agent

                ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
                                                 ||'-'||programacaoembarque.diferenciadornumero
                                                 ||'-'||programacaoembarque.numero
                                                 ||'-'||FNC_FORMATA_CNPJCPFCOD(notafiscalservico_calculofrete.destinatario)
                                                 ||'-'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
                        ) AS alternativeIdentifier

                ,COALESCE(notafiscalservico_calculofrete.dtprevisaoentrega,programacaoembarque.dtprevisaosaidaviagem)::DATE AS dateA

                ,janela.inicio AS hourA

                ,COALESCE(notafiscalservico_calculofrete.dtprevisaoentrega,programacaoembarque.dtprevisaosaidaviagem)::DATE AS executionForecastEndDate
                
                ,janela.fim AS executionForecastEndTime

                ,CONCAT('Remetente:'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
                        ||' '||'Quantidade:'||programacaoembarque.quantidade
                        ||' '||'Peso:'||programacaoembarque.peso
                        ||' '||'P.E:'||programacaoembarque.grupo
                        ||'-'||programacaoembarque.empresa
                        ||'-'||programacaoembarque.diferenciadornumero
                        ||'-'||programacaoembarque.numero
                ) AS observation

                ,30::integer AS situation

                ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
                                                 ||'-'||programacaoembarque.filialdocumentoorigem
                                                 ||'-'||programacaoembarque.unidadedocumentoorigem
                                                 ||'-'||programacaoembarque.diferenciadornumerodocumentoorigem
                                                 ||'-'||programacaoembarque.seriedocumentoorigem
                                                 ||'-'||programacaoembarque.numerodocumentoorigem
                        ) AS customField1

                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10) AS customField2
                ,programacaoembarque.veiculo AS tar_veiculo
                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10) AS tar_embarcador
                ,notafiscalservico.chaveacessorps AS listas_ctes

        FROM programacaoembarque

    LEFT JOIN programacaoembarque_composicao
            ON programacaoembarque.grupo = programacaoembarque_composicao.grupo
            AND programacaoembarque.empresa = programacaoembarque_composicao.empresa
            AND programacaoembarque.diferenciadornumero = programacaoembarque_composicao.diferenciadornumero
            AND programacaoembarque.numero = programacaoembarque_composicao.numero
            AND programacaoembarque_composicao.tipodocumento = 10

    LEFT JOIN notafiscalservico
            ON programacaoembarque_composicao.grupo = notafiscalservico.grupo
            AND programacaoembarque_composicao.empresa = notafiscalservico.empresa
            AND programacaoembarque_composicao.filialdocumento = notafiscalservico.filial
            AND programacaoembarque_composicao.unidadedocumento = notafiscalservico.unidade
            AND programacaoembarque_composicao.diferenciadornumerodocumento = notafiscalservico.diferenciadornumero
            AND programacaoembarque_composicao.seriedocumento = notafiscalservico.serie
            AND programacaoembarque_composicao.numerodocumento = notafiscalservico.numero
            

    LEFT JOIN notafiscalservico_calculofrete 
	   ON notafiscalservico_calculofrete.grupo = notafiscalservico.grupo
	   AND notafiscalservico_calculofrete.empresa = notafiscalservico.empresa
	   AND notafiscalservico_calculofrete.filial = notafiscalservico.filial
	   AND notafiscalservico_calculofrete.unidade = notafiscalservico.unidade
	   AND notafiscalservico_calculofrete.diferenciadornumero = notafiscalservico.diferenciadornumero
	   AND notafiscalservico_calculofrete.serie = notafiscalservico.serie
	   AND notafiscalservico_calculofrete.numero = notafiscalservico.numero 
    
      LEFT JOIN LATERAL(SELECT   codigo
                    ,max(ini) AS inicio
                    ,max(fim) AS fim 

                
                FROM ( SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebersegundafeira AS ini ,hrfinalcoletarrecebersegundafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                         UNION ALL
                       SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebertercafeira AS ini ,hrfinalcoletarrecebertercafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                         UNION ALL
                       SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarreceberquartafeira AS ini ,hrfinalcoletarreceberquartafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                         UNION ALL
                       SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarreceberquintafeira AS ini ,hrfinalcoletarreceberquintafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                         UNION ALL
                       SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebersextafeira AS ini ,hrfinalcoletarrecebersextafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                     ) as base
                    
                    GROUP BY codigo
                   )janela

            ON notafiscalservico_calculofrete.destinatario = janela.codigo

 WHERE programacaoembarque.numero < 1000000 
    AND programacaoembarque.unidade = 1
    AND programacaoembarque.dtemissao::date = now()::date
    AND notafiscalservico.chaveacessorps IS NOT NULL
    AND SUBSTRING(notafiscalservico_calculofrete.destinatario,1,8) = '96662168'
    AND notafiscalservico_calculofrete.remetente = '96662168016992'    
    ) as base

---where customfield1 = '1-1-1-1-1-1-109656'
---where tar_veiculo ='INQ8E54'



group by 
    scheduletype
    ,serviceLocal
    ,team
    ,teamExecution
    ,agent
    ,alternativeIdentifier
    ,dateA
    ,hourA
    ,executionForecastEndDate
    ,executionForecastEndTime
    ,observation
    ,situation
    ,customfield1
    ,customfield2
    ,tar_veiculo
    ,tar_embarcador
    
    """



items=""" 

SELECT
	description
	,alternativeIdentifier
	,schedule
	

FROM ( SELECT   
	    'notas_fiscais'::TEXT AS subGroup
	    ,CONCAT('CT-e'::TEXT||' '||conhecimento.numero) AS description
	    ,conhecimento.chaveacessocte AS alternativeIdentifier
	    ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
					     ||'-'||programacaoembarque.diferenciadornumero
					     ||'-'||programacaoembarque.numero
					     ||'-'||FNC_FORMATA_CNPJCPFCOD(conhecimento.destinatario)
					     ||'-'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
		   ) AS schedule
          

FROM programacaoembarque


LEFT JOIN programacaoembarque_composicao
	ON programacaoembarque.grupo = programacaoembarque_composicao.grupo
	AND programacaoembarque.empresa = programacaoembarque_composicao.empresa
	AND programacaoembarque.diferenciadornumero = programacaoembarque_composicao.diferenciadornumero
	AND programacaoembarque.numero = programacaoembarque_composicao.numero
	AND programacaoembarque_composicao.tipodocumento = 6 --cte

LEFT JOIN conhecimento
	ON programacaoembarque_composicao.grupo = conhecimento.grupo
	AND programacaoembarque_composicao.empresa = conhecimento.empresa
	AND programacaoembarque_composicao.filialdocumento = conhecimento.filial
	AND programacaoembarque_composicao.unidadedocumento = conhecimento.unidade
	AND programacaoembarque_composicao.diferenciadornumerodocumento = conhecimento.diferenciadornumero
	AND programacaoembarque_composicao.seriedocumento = conhecimento.serie
	AND programacaoembarque_composicao.numerodocumento = conhecimento.numero
 
WHERE programacaoembarque.numero < 1000000 
	AND programacaoembarque.unidade = 1
	AND programacaoembarque.dtemissao::date = now()::date
	AND conhecimento.chaveacessocte IS NOT NULL
        AND SUBSTRING(conhecimento.destinatario,1,8) = '96662168'
        AND conhecimento.remetente = '96662168016992'
----------------------------------------  NOTA FISCAL DE SERVIÇO ---------------------------------------
UNION ALL

SELECT   
	    'notas_fiscais'::TEXT AS subGroup
	    ,CONCAT('NFS-e'::TEXT||' '||notafiscalservico.numero) AS description
	    ,notafiscalservico.chaveacessorps AS alternativeIdentifier
	    ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
					     ||'-'||programacaoembarque.diferenciadornumero
					     ||'-'||programacaoembarque.numero
					     ||'-'||FNC_FORMATA_CNPJCPFCOD(notafiscalservico_calculofrete.destinatario)
					     ||'-'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
		   ) AS schedule
            

FROM programacaoembarque


    LEFT JOIN programacaoembarque_composicao
	    ON programacaoembarque.grupo = programacaoembarque_composicao.grupo
	    AND programacaoembarque.empresa = programacaoembarque_composicao.empresa
	    AND programacaoembarque.diferenciadornumero = programacaoembarque_composicao.diferenciadornumero
            AND programacaoembarque.numero = programacaoembarque_composicao.numero
            AND programacaoembarque_composicao.tipodocumento = 10 --nfse

    LEFT JOIN notafiscalservico
            ON programacaoembarque_composicao.grupo = notafiscalservico.grupo
            AND programacaoembarque_composicao.empresa = notafiscalservico.empresa
            AND programacaoembarque_composicao.filialdocumento = notafiscalservico.filial
            AND programacaoembarque_composicao.unidadedocumento = notafiscalservico.unidade
            AND programacaoembarque_composicao.diferenciadornumerodocumento = notafiscalservico.diferenciadornumero
            AND programacaoembarque_composicao.seriedocumento = notafiscalservico.serie
            AND programacaoembarque_composicao.numerodocumento = notafiscalservico.numero
            

    LEFT JOIN notafiscalservico_calculofrete 
	   ON notafiscalservico_calculofrete.grupo = notafiscalservico.grupo
	   AND notafiscalservico_calculofrete.empresa = notafiscalservico.empresa
	   AND notafiscalservico_calculofrete.filial = notafiscalservico.filial
	   AND notafiscalservico_calculofrete.unidade = notafiscalservico.unidade
	   AND notafiscalservico_calculofrete.diferenciadornumero = notafiscalservico.diferenciadornumero
	   AND notafiscalservico_calculofrete.serie = notafiscalservico.serie
	   AND notafiscalservico_calculofrete.numero = notafiscalservico.numero 
    
 
WHERE programacaoembarque.numero < 1000000 
	AND programacaoembarque.unidade = 1
	AND programacaoembarque.dtemissao::date = now()::date
	AND notafiscalservico.chaveacessorps IS NOT NULL
        AND SUBSTRING(notafiscalservico_calculofrete.destinatario,1,8) = '96662168'
        AND notafiscalservico_calculofrete.remetente = '96662168016992'
	) as base


group by
	description
	,alternativeIdentifier
	,schedule

"""

entregashora="""
SELECT
        scheduletype
        ,serviceLocal
        ,team
        ,teamExecution
        ,agent
        ,alternativeIdentifier
        ,dateA

        ,CASE WHEN (TO_CHAR(hourA,'HH24:MI')) IS NULL
                    THEN '00:00' else (TO_CHAR(hourA,'HH24:MI'))   
         END AS hourA

         ,executionForecastEndDate

         ,CASE WHEN (TO_CHAR(executionForecastEndTime,'HH24:MI')) IS NULL
                    THEN '00:00' else (TO_CHAR(executionForecastEndTime,'HH24:MI')) 
         END AS executionForecastEndTime
         
         ,observation
         ,situation
         ,customfield1
         ,customfield2
         ,tar_veiculo
         ,tar_embarcador
         ,STRING_AGG(listas_ctes,'/') as listas_ctes

 

FROM(   SELECT 
                'entrega'::TEXT AS scheduleType
                ,FNC_FORMATA_CNPJCPFCOD(conhecimento.destinatario) AS serviceLocal
                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque.cnpjcpfcodigoveiculo),1,10) AS team
                ,0::integer AS teamExecution
                ,FNC_FORMATA_CNPJCPFCOD(programacaoembarque.motorista) AS agent

                ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
                                                 ||'-'||programacaoembarque.diferenciadornumero
                                                 ||'-'||programacaoembarque.numero
                                                 ||'-'||FNC_FORMATA_CNPJCPFCOD(conhecimento.destinatario)
                                                 ||'-'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
                        ) AS alternativeIdentifier

                ,COALESCE(conhecimento.dtprevisaoentrega,programacaoembarque.dtprevisaosaidaviagem)::DATE AS dateA

                ,janela.inicio AS hourA

                ,COALESCE(conhecimento.dtprevisaoentrega,programacaoembarque.dtprevisaosaidaviagem)::DATE AS executionForecastEndDate
                
                ,janela.fim AS executionForecastEndTime

                ,CONCAT('Remetente:'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
                        ||' '||'Quantidade:'||programacaoembarque.quantidade
                        ||' '||'Peso:'||programacaoembarque.peso
                        ||' '||'P.E:'||programacaoembarque.grupo
                        ||'-'||programacaoembarque.empresa
                        ||'-'||programacaoembarque.diferenciadornumero
                        ||'-'||programacaoembarque.numero
                ) AS observation

                ,30::integer AS situation

                ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
                                                 ||'-'||programacaoembarque.filialdocumentoorigem
                                                 ||'-'||programacaoembarque.unidadedocumentoorigem
                                                 ||'-'||programacaoembarque.diferenciadornumerodocumentoorigem
                                                 ||'-'||programacaoembarque.seriedocumentoorigem
                                                 ||'-'||programacaoembarque.numerodocumentoorigem
                        ) AS customField1

                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10) AS customField2
                ,programacaoembarque.veiculo AS tar_veiculo
                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10) AS tar_embarcador
                ,conhecimento.chaveacessocte AS listas_ctes

        FROM programacaoembarque

    LEFT JOIN programacaoembarque_composicao
            ON programacaoembarque.grupo = programacaoembarque_composicao.grupo
            AND programacaoembarque.empresa = programacaoembarque_composicao.empresa
            AND programacaoembarque.diferenciadornumero = programacaoembarque_composicao.diferenciadornumero
            AND programacaoembarque.numero = programacaoembarque_composicao.numero
            AND programacaoembarque_composicao.tipodocumento = 6

    LEFT JOIN conhecimento
            ON programacaoembarque_composicao.grupo = conhecimento.grupo
            AND programacaoembarque_composicao.empresa = conhecimento.empresa
            AND programacaoembarque_composicao.filialdocumento = conhecimento.filial
            AND programacaoembarque_composicao.unidadedocumento = conhecimento.unidade
            AND programacaoembarque_composicao.diferenciadornumerodocumento = conhecimento.diferenciadornumero
            AND programacaoembarque_composicao.seriedocumento = conhecimento.serie
            AND programacaoembarque_composicao.numerodocumento = conhecimento.numero
            
    
    LEFT JOIN LATERAL(SELECT   codigo
                                ,max(ini) AS inicio
                                ,max(fim) AS fim 

                    
                        FROM ( SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebersegundafeira AS ini ,hrfinalcoletarrecebersegundafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                                     UNION ALL
                               SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebertercafeira AS ini ,hrfinalcoletarrecebertercafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                                     UNION ALL
                               SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarreceberquartafeira AS ini ,hrfinalcoletarreceberquartafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                                     UNION ALL
                               SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarreceberquintafeira AS ini ,hrfinalcoletarreceberquintafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                                     UNION ALL
                               SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebersextafeira AS ini ,hrfinalcoletarrecebersextafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                             ) as base
                            
                                GROUP BY codigo
                       )janela

            ON conhecimento.destinatario = janela.codigo

 WHERE programacaoembarque.numero < 1000000 
    AND programacaoembarque.unidade = 1
    AND programacaoembarque.dtemissao >= (NOW() - interval '30 minutes') AND programacaoembarque.dtemissao <= NOW()
    AND SUBSTRING(conhecimento.destinatario,1,8) = '96662168'
    AND conhecimento.remetente = '96662168016992'

----------------------------------------  NOTA FISCAL DE SERVIÇO ---------------------------------------
UNION ALL


	SELECT 
                'entrega'::TEXT AS scheduleType
                ,FNC_FORMATA_CNPJCPFCOD(notafiscalservico_calculofrete.destinatario) AS serviceLocal
                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque.cnpjcpfcodigoveiculo),1,10) AS team
                ,0::integer AS teamExecution
                ,FNC_FORMATA_CNPJCPFCOD(programacaoembarque.motorista) AS agent

                ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
                                                 ||'-'||programacaoembarque.diferenciadornumero
                                                 ||'-'||programacaoembarque.numero
                                                 ||'-'||FNC_FORMATA_CNPJCPFCOD(notafiscalservico_calculofrete.destinatario)
                                                 ||'-'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
                        ) AS alternativeIdentifier

                ,COALESCE(notafiscalservico_calculofrete.dtprevisaoentrega,programacaoembarque.dtprevisaosaidaviagem)::DATE AS dateA

                ,janela.inicio AS hourA

                ,COALESCE(notafiscalservico_calculofrete.dtprevisaoentrega,programacaoembarque.dtprevisaosaidaviagem)::DATE AS executionForecastEndDate
                
                ,janela.fim AS executionForecastEndTime

                ,CONCAT('Remetente:'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
                        ||' '||'Quantidade:'||programacaoembarque.quantidade
                        ||' '||'Peso:'||programacaoembarque.peso
                        ||' '||'P.E:'||programacaoembarque.grupo
                        ||'-'||programacaoembarque.empresa
                        ||'-'||programacaoembarque.diferenciadornumero
                        ||'-'||programacaoembarque.numero
                ) AS observation

                ,30::integer AS situation

                ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
                                                 ||'-'||programacaoembarque.filialdocumentoorigem
                                                 ||'-'||programacaoembarque.unidadedocumentoorigem
                                                 ||'-'||programacaoembarque.diferenciadornumerodocumentoorigem
                                                 ||'-'||programacaoembarque.seriedocumentoorigem
                                                 ||'-'||programacaoembarque.numerodocumentoorigem
                        ) AS customField1

                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10) AS customField2
                ,programacaoembarque.veiculo AS tar_veiculo
                ,SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10) AS tar_embarcador
                ,notafiscalservico.chaveacessorps AS listas_ctes

        FROM programacaoembarque

    LEFT JOIN programacaoembarque_composicao
            ON programacaoembarque.grupo = programacaoembarque_composicao.grupo
            AND programacaoembarque.empresa = programacaoembarque_composicao.empresa
            AND programacaoembarque.diferenciadornumero = programacaoembarque_composicao.diferenciadornumero
            AND programacaoembarque.numero = programacaoembarque_composicao.numero
            AND programacaoembarque_composicao.tipodocumento = 10

    LEFT JOIN notafiscalservico
            ON programacaoembarque_composicao.grupo = notafiscalservico.grupo
            AND programacaoembarque_composicao.empresa = notafiscalservico.empresa
            AND programacaoembarque_composicao.filialdocumento = notafiscalservico.filial
            AND programacaoembarque_composicao.unidadedocumento = notafiscalservico.unidade
            AND programacaoembarque_composicao.diferenciadornumerodocumento = notafiscalservico.diferenciadornumero
            AND programacaoembarque_composicao.seriedocumento = notafiscalservico.serie
            AND programacaoembarque_composicao.numerodocumento = notafiscalservico.numero
            

    LEFT JOIN notafiscalservico_calculofrete 
	   ON notafiscalservico_calculofrete.grupo = notafiscalservico.grupo
	   AND notafiscalservico_calculofrete.empresa = notafiscalservico.empresa
	   AND notafiscalservico_calculofrete.filial = notafiscalservico.filial
	   AND notafiscalservico_calculofrete.unidade = notafiscalservico.unidade
	   AND notafiscalservico_calculofrete.diferenciadornumero = notafiscalservico.diferenciadornumero
	   AND notafiscalservico_calculofrete.serie = notafiscalservico.serie
	   AND notafiscalservico_calculofrete.numero = notafiscalservico.numero 
    
      LEFT JOIN LATERAL(SELECT   codigo
                    ,max(ini) AS inicio
                    ,max(fim) AS fim 

                
                FROM ( SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebersegundafeira AS ini ,hrfinalcoletarrecebersegundafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                         UNION ALL
                       SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebertercafeira AS ini ,hrfinalcoletarrecebertercafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                         UNION ALL
                       SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarreceberquartafeira AS ini ,hrfinalcoletarreceberquartafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                         UNION ALL
                       SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarreceberquintafeira AS ini ,hrfinalcoletarreceberquintafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                         UNION ALL
                       SELECT cnpjcpfcodigo AS codigo ,hrinicialcoletarrecebersextafeira AS ini ,hrfinalcoletarrecebersextafeira AS fim FROM cadastro_vinculo_clienteapoiologistico
                     ) as base
                    
                    GROUP BY codigo
                   )janela

            ON notafiscalservico_calculofrete.destinatario = janela.codigo

 WHERE programacaoembarque.numero < 1000000 
    AND programacaoembarque.unidade = 1
    AND programacaoembarque.dtemissao >= (NOW() - interval '30 minutes') AND programacaoembarque.dtemissao <= NOW()
    AND notafiscalservico.chaveacessorps IS NOT NULL
    AND SUBSTRING(notafiscalservico_calculofrete.destinatario,1,8) = '96662168'
    AND notafiscalservico_calculofrete.remetente = '96662168016992'

    ) as base

--where tar_veiculo = 'JOL7184'
--where customfield1 = '1-1-1-1-1-1-109075'

group by 
    scheduletype
    ,serviceLocal
    ,team
    ,teamExecution
    ,agent
    ,alternativeIdentifier
    ,dateA
    ,hourA
    ,executionForecastEndDate
    ,executionForecastEndTime
    ,observation
    ,situation
    ,customfield1
    ,customfield2
    ,tar_veiculo
    ,tar_embarcador
    
    """

itemshora=""" 

SELECT
	description
	,alternativeIdentifier
	,schedule
	

FROM ( SELECT   
	    'notas_fiscais'::TEXT AS subGroup
	    ,CONCAT('CT-e'::TEXT||' '||conhecimento.numero) AS description
	    ,conhecimento.chaveacessocte AS alternativeIdentifier
	    ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
					     ||'-'||programacaoembarque.diferenciadornumero
					     ||'-'||programacaoembarque.numero
					     ||'-'||FNC_FORMATA_CNPJCPFCOD(conhecimento.destinatario)
					     ||'-'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
		   ) AS schedule
          

FROM programacaoembarque


LEFT JOIN programacaoembarque_composicao
	ON programacaoembarque.grupo = programacaoembarque_composicao.grupo
	AND programacaoembarque.empresa = programacaoembarque_composicao.empresa
	AND programacaoembarque.diferenciadornumero = programacaoembarque_composicao.diferenciadornumero
	AND programacaoembarque.numero = programacaoembarque_composicao.numero
	AND programacaoembarque_composicao.tipodocumento = 6 --cte

LEFT JOIN conhecimento
	ON programacaoembarque_composicao.grupo = conhecimento.grupo
	AND programacaoembarque_composicao.empresa = conhecimento.empresa
	AND programacaoembarque_composicao.filialdocumento = conhecimento.filial
	AND programacaoembarque_composicao.unidadedocumento = conhecimento.unidade
	AND programacaoembarque_composicao.diferenciadornumerodocumento = conhecimento.diferenciadornumero
	AND programacaoembarque_composicao.seriedocumento = conhecimento.serie
	AND programacaoembarque_composicao.numerodocumento = conhecimento.numero
 
WHERE programacaoembarque.numero < 1000000 
	AND programacaoembarque.unidade = 1
	AND programacaoembarque.dtemissao >= (NOW() - interval '30 minutes') AND programacaoembarque.dtemissao <= NOW()
	AND conhecimento.chaveacessocte IS NOT NULL
        AND SUBSTRING(conhecimento.destinatario,1,8) = '96662168'
        AND conhecimento.remetente = '96662168016992'
----------------------------------------  NOTA FISCAL DE SERVIÇO ---------------------------------------
UNION ALL

SELECT   
	    'notas_fiscais'::TEXT AS subGroup
	    ,CONCAT('NFS-e'::TEXT||' '||notafiscalservico.numero) AS description
	    ,notafiscalservico.chaveacessorps AS alternativeIdentifier
	    ,CONCAT(programacaoembarque.grupo||'-'||programacaoembarque.empresa
					     ||'-'||programacaoembarque.diferenciadornumero
					     ||'-'||programacaoembarque.numero
					     ||'-'||FNC_FORMATA_CNPJCPFCOD(notafiscalservico_calculofrete.destinatario)
					     ||'-'||SUBSTRING(FNC_FORMATA_CNPJCPFCOD(programacaoembarque_composicao.cnpjcpfcodigoemissordocumento),1,10)
		   ) AS schedule
            

FROM programacaoembarque


    LEFT JOIN programacaoembarque_composicao
	    ON programacaoembarque.grupo = programacaoembarque_composicao.grupo
	    AND programacaoembarque.empresa = programacaoembarque_composicao.empresa
	    AND programacaoembarque.diferenciadornumero = programacaoembarque_composicao.diferenciadornumero
            AND programacaoembarque.numero = programacaoembarque_composicao.numero
            AND programacaoembarque_composicao.tipodocumento = 10 --nfse

    LEFT JOIN notafiscalservico
            ON programacaoembarque_composicao.grupo = notafiscalservico.grupo
            AND programacaoembarque_composicao.empresa = notafiscalservico.empresa
            AND programacaoembarque_composicao.filialdocumento = notafiscalservico.filial
            AND programacaoembarque_composicao.unidadedocumento = notafiscalservico.unidade
            AND programacaoembarque_composicao.diferenciadornumerodocumento = notafiscalservico.diferenciadornumero
            AND programacaoembarque_composicao.seriedocumento = notafiscalservico.serie
            AND programacaoembarque_composicao.numerodocumento = notafiscalservico.numero
            

    LEFT JOIN notafiscalservico_calculofrete 
	   ON notafiscalservico_calculofrete.grupo = notafiscalservico.grupo
	   AND notafiscalservico_calculofrete.empresa = notafiscalservico.empresa
	   AND notafiscalservico_calculofrete.filial = notafiscalservico.filial
	   AND notafiscalservico_calculofrete.unidade = notafiscalservico.unidade
	   AND notafiscalservico_calculofrete.diferenciadornumero = notafiscalservico.diferenciadornumero
	   AND notafiscalservico_calculofrete.serie = notafiscalservico.serie
	   AND notafiscalservico_calculofrete.numero = notafiscalservico.numero 
    
 
WHERE programacaoembarque.numero < 1000000 
	AND programacaoembarque.unidade = 1
	AND programacaoembarque.dtemissao >= (NOW() - interval '30 minutes') AND programacaoembarque.dtemissao <= NOW()
	AND notafiscalservico.chaveacessorps IS NOT NULL
        AND SUBSTRING(notafiscalservico_calculofrete.destinatario,1,8) = '96662168'
        AND notafiscalservico_calculofrete.remetente = '96662168016992'
 
	) as base


group by
	description
	,alternativeIdentifier
	,schedule

"""