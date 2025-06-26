# 🌱 Deledan: Guardian of the Verdant Cycle

**Versão:** 1.0  
**Data:** 26 de Junho de 2025  
**Linguagem:** Python 3 com [Pygame](https://www.pygame.org/) e [NumPy](https://numpy.org/)

---

## 👥 Autores e Funções

- **Calebe Araujo** & **Cleiton Valentim** — Programação
- **Ivo Sousa**, **Gabriel Teruel** & **Eliabe Ramos** — Roteiro e Narrativa
- **Ivo Sousa** — Pesquisa sobre linguagem e tecnologias usadas

---

## 🌿 Visão Geral

**Deledan: Guardian of the Verdant Cycle** é um jogo 2D de **ação e sobrevivência** com temática ecológica e estética retrô. Desenvolvido inteiramente em **Python**, o projeto se destaca por **gerar todos os gráficos e sons por código**, sem uso de imagens ou arquivos externos.

Você é o Guardião de Deledan, a Floresta Ancestral, e precisa sobreviver ao avanço de uma praga misteriosa, restaurando o equilíbrio do ciclo da vida.

---

## 📖 História

Antes do tempo moderno, existia Deledan — uma floresta mágica e viva, guardiã do ciclo da vida. A cada geração, um Guardião era escolhido para protegê-la.

Agora, Deledan está corrompida por uma praga sombria. Você é o último Guardião, despertado para proteger a floresta, derrotar as sombras e restaurar a harmonia.

---

## 🕹️ Funcionalidades Principais

- 🔁 **Mapas Gerados Proceduralmente**  
  Cada jogada é única, com mapas diferentes a cada transição de tela.

- ⏫ **Dificuldade Progressiva**  
  Inimigos mais rápidos e numerosos com o tempo de sobrevivência.

- ❤️ **Sistema de Vida e Power-ups**  
  Colete *Sementes de Vida* para recuperar HP.

- 🌱 **Arma Temporária**  
  Após 30s de jogo, você desbloqueia a *Arma de Sementes* por tempo limitado.

- 💥 **Física de Colisão Robusta**  
  Verificação nos quatro cantos para evitar bugs e travamentos.

- ✅ **Spawn Seguro**  
  O jogador sempre nasce em locais livres de obstáculos.

- 🧠 **Gráficos e Sons 100% Procedurais**  
  Tudo criado com `pygame.draw` e `NumPy`, gerando um estilo retrô único.

- 📜 **Menu Interativo Completo**  
  História inicial, tela principal, gameplay e tela de fim de jogo.

---

## 🎮 Como Jogar

### Controles:

| Tecla         | Função                        |
|---------------|-------------------------------|
| W, A, S, D     | Movimentar o personagem       |
| Espaço         | Dash (movimento rápido)       |
| F              | Disparo com Arma de Sementes  |
| R              | Reiniciar após Game Over      |
| Enter          | Avançar a tela de história     |
| Mouse          | Navegação nos menus           |

### Objetivo:

**Sobreviva o maior tempo possível!**  
Pontue sobrevivendo, colete sementes e use a arma especial para enfrentar a praga.

---

## ⚙️ Instalação e Execução

### Pré-requisitos:

- Python 3.x  
- Bibliotecas:
  - `pygame`
  - `numpy`

### Instalação das dependências:

```bash
pip install pygame
pip install numpy


📂 Estrutura do Código

Tudo está contido em um único arquivo Main.py para facilitar a organização.

	•	Inicialização e Constantes: Configurações de tela, cores e variáveis globais.
	•	Geração de Som: Sons criados por código usando NumPy.
	•	Funções Visuais: Desenho de elementos como jogador, inimigos, partículas, etc.
	•	Classes:
	•	Player: Controle do personagem.
	•	Enemy: Comportamento dos inimigos.
	•	PowerUp, Seed, Particle: Objetos dinâmicos do jogo.
	•	Game: Classe principal que gerencia todo o jogo.
	•	Máquina de Estados: Gerencia os estados: história, menu, gameplay e fim de jogo.
	•	Função main(): Loop principal do jogo — eventos, atualização e desenho.

⸻

🔮 Melhorias Futuras
	•	👾 Novos inimigos: Com padrões de movimento e ataques variados.
	•	⚡ Power-ups adicionais: Invencibilidade, congelamento de inimigos, velocidade extra.
	•	🧠 Chefes (Bosses): Enfrente grandes inimigos após determinado tempo.
	•	🎵 Trilha Sonora Procedural: Música dinâmica que reage ao jogo.
	•	🏆 Sistema de Pontuação Avançado: Recompensas por derrotar inimigos.
	•	💾 Salvar Recordes: Armazene a melhor pontuação localmente.

⸻

🎉 DeleDan: Guardião do Ciclo Verdejante – O Jogo!

Um projeto acadêmico com coração indie, feito por estudantes apaixonados por natureza, jogos e código puro. 🌳💚
Obrigado por jogar!

⸻

📌 Licença

Este projeto é livre para uso acadêmico e pessoal. Para fins comerciais, entre em contato com os autores.
