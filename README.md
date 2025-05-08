# UtilitariosPython

O projeto tem o intuito de agrupar algumas funcionalidades em python que podem ser repetidas e simplifica-lás o máximo o possível.

Cada uma das pastas listadas dentro do projeto é indepente uma da outra.

## GerenciadorTarefas
```pyton
from GerenciadorTarefas.GerenciadorTarefas import Tarefa, Disparador, Acao

Tarefa("Teste", disparadores=[Disparador(9, 5)], acoes=[Acao('C:\\Users\\usuario\\Desktop\\Novo Texto.txt')])
```

## MongoDriver
```pyton
from MongoDriver.MongoDriver import MDriver

driver = MDriver("localhost", "banco", "colecao")
```

## NotificadorEmail
```pyton
from NotificadorEmail.NotificadorEmail import NEmail

NEmail("ola", "de@email.com.br", "para@email.com.br", "senha1234", anexos=['C:\\Users\\usuario\\Desktop\\Novo Texto.txt'])
```

## NotificadorWindows
```pyton
from NotificadorWindows.NotificadorWindows import NWindows

NWindows("Teste", "ola", icone="C:\\Users\\usuario\\Desktop\\Sem título.png", executar="C:\\Program Files\\Notepad++\\notepad++.exe")
```

## SeleniumDriver
```pyton
from SeleniumDriver.SeleniumDriver import SDriver

driver = SDriver("https://site.com/")
```
