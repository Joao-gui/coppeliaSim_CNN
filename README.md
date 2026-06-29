# 🤖 CoppeliaSim + MobileNet

Projeto desenvolvido como parte do desafio proposto na **WebConf01** da disciplina de **Introdução à Robótica**, pertencente ao curso de Pós-Graduação em Inteligência Artificial (Turma VI), ministrada pela **Prof.ª Natássya Barlate**.

O projeto integra técnicas de **Visão Computacional**, **Deep Learning** e **Robótica**, utilizando uma **Rede Neural Convolucional (CNN)** para que um robô simulado no **CoppeliaSim** seja capaz de reconhecer objetos presentes no ambiente.

O robô percorre o cenário identificando dois objetos:

* 🔺 Cone Vermelho
* 🟥 Cubo Vermelho

Embora ambos sejam reconhecidos pela rede neural, apenas as detecções do **Cone Vermelho** são registradas no gráfico de resultados, conforme especificado no desafio.

---

# 📌 Objetivos

* Integrar o CoppeliaSim com Python;
* Aplicar uma CNN para classificação de imagens em tempo real;
* Reconhecer objetos presentes no ambiente de simulação;
* Demonstrar a aplicação de Inteligência Artificial em Robótica;
* Validar o funcionamento da rede neural durante a navegação do robô.

---

# 🧠 Lógica Utilizada

Para realizar a classificação das imagens foi utilizada a **MobileNet**, uma Rede Neural Convolucional pré-treinada no conjunto de dados **ImageNet**.

A utilização de uma rede pré-treinada permite aproveitar características já aprendidas durante seu treinamento, reduzindo o tempo de desenvolvimento e eliminando a necessidade de treinar uma CNN do zero. Quando necessário, apenas as últimas camadas podem ser ajustadas utilizando a técnica de **Transfer Learning**.

A escolha da MobileNet ocorreu devido às suas principais características:

* Modelo leve;
* Alta velocidade de inferência;
* Baixo consumo de memória;
* Excelente desempenho para aplicações em tempo real;
* Ideal para robótica e sistemas embarcados.

Essas características tornam a MobileNet mais adequada para este projeto do que arquiteturas mais robustas, como a ResNet.

---

# 🛠 Tecnologias utilizadas

* Python 3
* TensorFlow / Keras
* MobileNet
* OpenCV
* NumPy
* CoppeliaSim
* ZeroMQ Remote API

---

# 📂 Estrutura do projeto

```text
coppeliaSim_CNN/
│
├── cena_coppelia/                # Cena utilizada no Coppelia para o projeto
├── dataset/                      # Pasta com as imagens de Treino/Teste/Validação
├── mapping/                      # Script do mapa gerado no coppleia
├── models/                       # Modelo gerado do treinamento da CNN
├── notebooks/		          # Notebooks de treino/geração de modelo e teste
├── simulation/		          # Script do RemoteAPI
├── vision/		          # Script da configuração do sensor de visão do robo
├── .gitignore
├── main.py                       # Script principal
├── requirements.txt
├── LICENSE
└── README.md
```

---

# 🚀 Como executar

## 1. Clone o repositório

```bash
git clone https://github.com/Joao-gui/coppeliaSim_CNN.git

cd coppeliaSim_CNN
```

## 2. Crie um ambiente virtual

### Linux

```bash
python -m venv .venv

source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

---

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 4. Execute o CoppeliaSim

Abra a cena do projeto e inicie a simulação.

---

## 5. Execute o projeto

```bash
python main.py
```

---

# 🧠 Fluxo do sistema

```text
Câmera do Robô
        │
        ▼
 Captura da imagem
        │
        ▼
 Pré-processamento
        │
        ▼
 MobileNet (CNN)
        │
        ▼
 Classificação do objeto
        │
        ▼
 Lógica de decisão
        │
        ▼
 Controle do robô
```

---

# 📷 Funcionamento

1. O robô percorre o ambiente virtual.
2. A câmera embarcada captura imagens continuamente.
3. As imagens são pré-processadas em Python.
4. A MobileNet realiza a classificação dos objetos.
5. O sistema identifica a presença do Cone Vermelho e do Cubo Vermelho.
6. Apenas as detecções do Cone Vermelho são registradas no gráfico, conforme os requisitos do desafio.

---

# 🎯 Aplicações

* Inteligência Artificial
* Machine Learning
* Deep Learning
* Visão Computacional
* Robótica
* Sistemas Embarcados
* Automação

---

# 📚 Aprendizados

Durante o desenvolvimento deste projeto foram aplicados conhecimentos de:

* Redes Neurais Convolucionais (CNN)
* Transfer Learning
* MobileNet
* Processamento de Imagens
* OpenCV
* TensorFlow/Keras
* Comunicação Python ↔ CoppeliaSim
* Simulação Robótica
* Inferência em tempo real

---

# 👨‍💻 Autor

**João Guilherme Pellacani**

Engenheiro Eletricista

Pós-graduando em Inteligência Artificial (UTFPR)

* GitHub: https://github.com/Joao-gui
* LinkedIn: https://www.linkedin.com/in/joaogpellacani/

---

# 📄 Licença

Este projeto está licenciado sob a licença MIT.
