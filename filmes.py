import streamlit as st
import requests
import random
import time

# Sua chave de API do TMDb
API_KEY = "d78f9edcc46b81eeaaf33881876d449e"  # Substitua pela sua chave de API
BASE_URL = "https://api.themoviedb.org/3"

# Função para buscar filmes por gênero e plataforma
def buscar_filmes_por_genero_e_plataforma(genero_id, plataforma_id, exclude_countries=None, year_range=None):
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "pt-BR",
        "with_genres": genero_id,
        "with_watch_providers": plataforma_id,
        "watch_region": "BR",
        "sort_by": "popularity.desc",
        "page": random.randint(1, 5)
    }
    
    # Adicionar filtro por países excluídos
    if exclude_countries:
        params["without_original_country"] = ",".join(exclude_countries)
    
    # Adicionar filtro por intervalo de anos
    if year_range:
        params["primary_release_date.gte"] = f"{year_range[0]}-01-01"
        params["primary_release_date.lte"] = f"{year_range[1]}-12-31"
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()["results"]
    else:
        st.error(f"Erro ao buscar filmes. Código de status: {response.status_code}")
        return []

# Função para buscar séries por gênero e plataforma
def buscar_series_por_genero_e_plataforma(genero_id, plataforma_id, exclude_countries=None, year_range=None):
    url = f"{BASE_URL}/discover/tv"
    params = {
        "api_key": API_KEY,
        "language": "pt-BR",
        "with_genres": genero_id,
        "with_watch_providers": plataforma_id,
        "watch_region": "BR",
        "sort_by": "popularity.desc",
        "page": random.randint(1, 5)
    }
    
    # Adicionar filtro por países excluídos
    if exclude_countries:
        params["without_original_country"] = ",".join(exclude_countries)
    
    # Adicionar filtro por intervalo de anos
    if year_range:
        params["first_air_date.gte"] = f"{year_range[0]}-01-01"
        params["first_air_date.lte"] = f"{year_range[1]}-12-31"
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()["results"]
    else:
        st.error(f"Erro ao buscar séries. Código de status: {response.status_code}")
        return []

# Função para buscar filmes/séries pelo nome
def buscar_por_nome(nome, tipo):
    url = f"{BASE_URL}/search/{'movie' if tipo == 'Filme' else 'tv'}"
    params = {
        "api_key": API_KEY,
        "language": "pt-BR",
        "query": nome,
        "page": 1
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()["results"]
    else:
        st.error(f"Erro ao buscar {tipo.lower()}. Código de status: {response.status_code}")
        return []

# Função para buscar plataformas de streaming
def buscar_plataformas(tipo, id):
    url = f"{BASE_URL}/{tipo}/{id}/watch/providers"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", {}).get("BR", {})  # Dados para o Brasil
    else:
        st.error(f"Erro ao buscar plataformas. Código de status: {response.status_code}")
        return {}

# Função para simular a roleta
def roleta(lista, tipo_aleatorio, placeholder):
    # Escolhe um item aleatório da lista
    escolha_final = random.choice(lista)
    
    # Tempo total da roleta (6 segundos)
    tempo_total = 6.0
    inicio = time.time()
    
    while True:
        # Calcula o tempo restante
        tempo_decorrido = time.time() - inicio
        if tempo_decorrido >= tempo_total:
            break
        
        # Escolhe um item aleatório da lista
        item_aleatorio = random.choice(lista)
        if tipo_aleatorio == "Filme":
            titulo = item_aleatorio.get("title")
        else:
            titulo = item_aleatorio.get("name")
        
        # Exibe o título atual com efeito de roleta
        placeholder.markdown(
            f"""
            <div style=\"text-align: center; font-size: 24px; padding: 20px; border: 2px solid #FF4B4B; border-radius: 10px;\">
                🎡 {titulo}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Aumenta o tempo entre cada "giro" para simular a desaceleração
        time.sleep(0.1 * (tempo_decorrido + 1))
    
    # Exibe o resultado final
    if tipo_aleatorio == "Filme":
        titulo_final = escolha_final.get("title")
    else:
        titulo_final = escolha_final.get("name")
    
    placeholder.markdown(
        f"""
        <div style=\"text-align: center; font-size: 32px; padding: 20px; border: 2px solid #FF4B4B; border-radius: 10px; background-color: #FF4B4B;\">
            🎉 {titulo_final}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Exibe a imagem do filme/série escolhido
    if escolha_final.get("poster_path"):
        st.image(f"https://image.tmdb.org/t/p/w500{escolha_final['poster_path']}", width=300)
    
    # Exibe as plataformas de streaming
    plataformas = buscar_plataformas("movie" if tipo_aleatorio == "Filme" else "tv", escolha_final["id"])
    if plataformas:
        st.write("### Plataformas de Streaming")
        if plataformas.get("flatrate"):
            st.write("Disponível em:")
            for provider in plataformas["flatrate"]:
                st.write(f"- {provider['provider_name']}")
        else:
            st.write("Não disponível em streaming no momento.")

# Dicionário de gêneros (IDs do TMDb)
GENEROS = {
    "Ação": 28,
    "Comédia": 35,
    "Terror": 27,
    "Drama": 18,
    "Ficção Científica": 878,
    "Animação": 16,
    "Romance": 10749
}

# Dicionário de plataformas (IDs do TMDb)
PLATAFORMAS = {
    "Todas as Plataformas": None,  # Opção para buscar em todas as plataformas
    "Netflix": 8,
    "Max": 1899,
    "Paramount+": 531,
    "Prime Video": 9,
    "Disney+": 337,
    "Apple TV+": 350
}

# Dicionário de países (códigos ISO 3166-1 alpha-2)
PAISES = {
    "Estados Unidos": "US",
    "Brasil": "BR",
    "Reino Unido": "GB",
    "Canadá": "CA",
    "França": "FR",
    "Alemanha": "DE",
    "Índia": "IN",
    "Japão": "JP",
    "Coreia do Sul": "KR",
    "Austrália": "AU"
}

# Configuração do tema escuro
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título do aplicativo
st.title("👾 Escolha seu filme/série 👾")

# Sidebar para escolher plataformas
st.sidebar.title("Plataformas de Streaming")
plataforma_selecionada = st.sidebar.selectbox(
    "Escolha uma plataforma:",
    list(PLATAFORMAS.keys())
)

# Sidebar para escolher países a excluir
st.sidebar.title("Excluir Filmes/Séries de Países")
paises_excluidos = st.sidebar.multiselect(
    "Escolha os países a excluir:",
    list(PAISES.keys())
)

# Sidebar para escolher intervalo de anos
st.sidebar.title("Filtrar por Ano")
ano_inicial = st.sidebar.number_input("Ano inicial:", min_value=1900, max_value=2023, value=2000)
ano_final = st.sidebar.number_input("Ano final:", min_value=1900, max_value=2023, value=2023)

# Converter países selecionados para códigos ISO
exclude_countries = [PAISES[pais] for pais in paises_excluidos]

# Definir intervalo de anos
year_range = (ano_inicial, ano_final) if ano_inicial <= ano_final else None

# Opção de busca por nome
st.sidebar.title("Buscar por Nome")
nome_busca = st.sidebar.text_input("Digite o nome do filme/série:")
tipo_busca = st.sidebar.radio("Tipo:", ["Filme", "Série"])

# Opção de escolha aleatória no centro da tela
st.write("---")
st.header("🎲 Escolha Aleatória")

# Escolher entre filme ou série
tipo_aleatorio = st.radio("Escolha o tipo:", ["Filme", "Série"])

# Escolher um gênero
genero_aleatorio = st.selectbox("Escolha um gênero:", list(GENEROS.keys()))

# Botão para escolha aleatória geral
if st.button("Escolher aleatoriamente"):
    if plataforma_selecionada == "Todas as Plataformas":
        if tipo_aleatorio == "Filme":
            lista = buscar_filmes_por_genero_e_plataforma(GENEROS[genero_aleatorio], None, exclude_countries, year_range)
        else:
            lista = buscar_series_por_genero_e_plataforma(GENEROS[genero_aleatorio], None, exclude_countries, year_range)
    else:
        if tipo_aleatorio == "Filme":
            lista = buscar_filmes_por_genero_e_plataforma(GENEROS[genero_aleatorio], PLATAFORMAS[plataforma_selecionada], exclude_countries, year_range)
        else:
            lista = buscar_series_por_genero_e_plataforma(GENEROS[genero_aleatorio], PLATAFORMAS[plataforma_selecionada], exclude_countries, year_range)
    
    if lista:
        placeholder = st.empty()
        roleta(lista, tipo_aleatorio, placeholder)
    else:
        st.warning("Nenhum item encontrado para este gênero e plataforma.")

# Botão para buscar por nome
if nome_busca:
    resultados = buscar_por_nome(nome_busca, tipo_busca)
    if resultados:
        st.write(f"### Resultados para '{nome_busca}':")
        for item in resultados:
            st.write(f"**{item.get('title' if tipo_busca == 'Filme' else 'name')}**")
            if item.get("poster_path"):
                st.image(f"https://image.tmdb.org/t/p/w500{item['poster_path']}", width=200)
            st.write(item.get("overview"))
            st.write("---")
    else:
        st.warning("Nenhum resultado encontrado.")

st.write("---")

# Abas para gêneros
st.header("🎬 Catálogo por Gênero")
aba_generos = st.tabs(list(GENEROS.keys()))

for i, genero_nome in enumerate(GENEROS.keys()):
    with aba_generos[i]:
        st.write(f"### Filmes de {genero_nome}")
        if plataforma_selecionada == "Todas as Plataformas":
            filmes = buscar_filmes_por_genero_e_plataforma(GENEROS[genero_nome], None, exclude_countries, year_range)
        else:
            filmes = buscar_filmes_por_genero_e_plataforma(GENEROS[genero_nome], PLATAFORMAS[plataforma_selecionada], exclude_countries, year_range)
        
        if filmes:
            for item in filmes:
                st.write(f"**{item.get('title')}**")
                if item.get("poster_path"):
                    st.image(f"https://image.tmdb.org/t/p/w500{item['poster_path']}", width=200)
                st.write(item.get("overview"))
                st.write("---")
        else:
            st.warning("Nenhum filme encontrado para este gênero e plataforma.")
