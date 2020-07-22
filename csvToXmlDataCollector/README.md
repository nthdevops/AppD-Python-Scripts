# Guia de utilização do script

## Preparação para execução:

### Antes de iniciar o script é necessário o inserção de alguns arquivos na estrutura do diretório e respeitar os padrões determinados para o CSV como indicado abaixo:

**Templates:**
	No diretório onde o arquivo *main.py* está, crie o diretório **_templates_**.

	Dentro de templates, será necessário incluir o arquivo *csv* que será utilizado na criação dos Data Collectors.

	Novamente dentro de templates será necessário incluir os arquivos XML que correspondem ao export das applicações que estão presentes no csv:

		Exemplo: Dentro do arquivo csv existem as applications app1, app2, app3 que serão feitos Data Collectors. Vá no controller e exporte o xml de cada uma dessas applications.

		Caso não saiba fazer isso, veja no link: https://docs.appdynamics.com/display/PRO45/Export+and+Import+Business+Application+Settings

		Depois de exportar esses xmls, renomeie eles para o nome que está no csv. Logo o xml exportado da application app1, deve ser renomeado para app1.xml, e assim por diante para todas as applications.

	Realizado esses passos para todas as applications o script está pronto para funcionar.


**Padrão do CSV:**
	O CSV precisa ser separado por ";".

	O script prevê alguns cenários de csv para execução:

		O ideal, é que steja no padrão abaixo:

			applicationName;bunissesTransactions;class;method;getters

		applicationName: Nome da application que está no controller e que também será usada de referência para buscar os templates de xml. Como citado no exemplo acima, essa coluna teria valor "app1".

		bunissesTransactions: Todas as business transactions que farão uso do Data Collector, separadas por vírgula. Exemplo: /login,/,/auth.

		class: A classe de configuração do Data Collector.

		method: O método de configuração do Data Collector.

		getters: Todos os getters que são relacionados a classe e método de sua linha, separados por vírgula.

		Especificação dos getters:

			Uso dos getters para index:

			O getter pegando o index 0 do método sem nenhuma tratativa adicional, deve ser inserido da seguinte forma:

				app1;/login,/,/auth;com.class1;method1;param[0]

			O getter pegando o index 0 do método com tratativa adicional, deve ser inserido da seguinte forma:

				app1;/login,/,/auth;com.class1;method1;param[0].getDadoExemplo()

			O getter pegando o retorno do método sem nenhuma trativa adicional pode ser realizado das seguinte formas:

				app1;/login,/,/auth;com.class1;method1;toString
				OU
				app1;/login,/,/auth;com.class1;method1;

			A opção de deixar a célula vazia também é válida, porém será necessário ativar a validação do csv e caso haja alguma coleta adicional além do toString, será melhor utilizar toString, que ficará: getExemplo(),toString ao invés de um valor vazio.

			O getter pegando o retorno do método com trativa adicional, deve ser inserido da seguinte forma:

				app1;/login,/,/auth;com.class1;method1;getDadoExemplo()

			Tendo como exemplo as linhas de csv a seguir:

				app1;/login,/,/auth;com.class1;method1;param[0]

				app1;/login,/,/auth;com.class1;method1;param[1]

				No exemplo será necessário ativar a validação do csv, que irá processar as linhas e transformar para:

					app1;/login,/,/auth;com.class1;method1;param[0],param[1]

			Exemplos de getters:

				Index 2 com getter e retorno sem tratativa:

					app1;/login,/,/auth;com.class1;method1;param[2].getterExemplo(),toString

					No exemplo acima "param[2].getterExemplo()" é o index com getter e a presença do segundo getter "toString" diz ao script que o retorno do método deve ser coletado sem nenhuma tratativa adicional.

				Retorno no método com tratativa e index 1 sem tratativa:

					app1;/login,/,/auth;com.class1;method1;getterExemplo(),param[1]

					No exemplo acima "getterExemplo()" é o retorno com getter e a presença do segundo getter "param[1]" diz ao script que o index 1 do método deve ser coletado sem nenhuma tratativa adicional.

		Tendo a validação de csv ativa também pode-se usar mesclas de células, que irão ser tratadas.

## Execução:

### Para executar o script, abra um prompt de comando, vá até o diretório que o main.py file está e execute:
   **python main.py "nomeDoCsv.csv" "PREFIXO_NOME_DTS" VALIDARCSV(true/false) CRIARDATACOLLECTORSIMPORT(true/false) CRIARBUSINESSTRANSACTIONSIMPORT(true/false)** (Não é necessário adicionar /templates/nomeDoCsv.csv, apenas o nome do arquivo)

**Exemplos:**

	python main.py "nomeDoCsv.csv" PROJ1 true true true = O paramêtro PROJ1 define o prefixo para nomeação dos Data Collectors, o primeiro paramêtro "true" é para validar o CSV, o segundo para criar os xmls dos data collectors e o terceiro para criar os xmls das business transactions

	python main.py "nomeDoCsv.csv" PROJ2 false true true = O paramêtro PROJ2 define o prefixo para nomeação dos Data Collectors, o primeiro  paramêtro "false" diz que não irá validar o CSV, o segundo paramêtro "true" diz que irá criar os xmls dos data collectors e o terceiro para criar os xmls das business transactions