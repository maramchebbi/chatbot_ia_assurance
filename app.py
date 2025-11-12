import streamlit as st
import pickle
import numpy as np
from datetime import datetime
import os

# IMPORTANT : set_page_config DOIT être la PREMIÈRE commande Streamlit
st.set_page_config(
    page_title="Chatbot IA Assurance - Maram Chebbi",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Forcer le mode texte brut pour éviter regex bugs
os.environ['STREAMLIT_MARKDOWN_AUTOLINK'] = 'false'

@st.cache_resource
def load_chatbot_data():
    with open('chatbot_data.pkl', 'rb') as f:
        chatbot_data = pickle.load(f)
    with open('metadata.pkl', 'rb') as f:
        metadata = pickle.load(f)
    return chatbot_data, metadata

try:
    chatbot_data, metadata = load_chatbot_data()
    knowledge_base = chatbot_data['knowledge_base']
    faqs = chatbot_data['faqs']
    vectorizer = chatbot_data['vectorizer']
    faq_vectors = chatbot_data['faq_vectors']
    faq_questions = chatbot_data['faq_questions']
    faq_reponses = chatbot_data['faq_reponses']
    models_loaded = True
except:
    models_loaded = False

st.markdown("""
<style>
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        animation: fadeIn 0.5s;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    .bot-message {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #333;
        margin-right: 20%;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .product-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .suggestion-btn {
        background: #f0f2f6;
        border: 1px solid #667eea;
        color: #667eea;
        padding: 8px 15px;
        border-radius: 20px;
        margin: 5px;
        cursor: pointer;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Chatbot IA Assurance")
st.markdown("### Votre Assistant Intelligent pour l'Assurance")
st.write("Développé par : Maram Chebbi | ESPRIT & IRA Le Mans")
st.markdown("---")

if not models_loaded:
    st.error("⚠️ Erreur de chargement des données du chatbot")
    st.stop()

st.sidebar.header("🎯 Fonctionnalités")
st.sidebar.markdown("""
- 💬 **Chat Intelligent** : Posez vos questions
- 💰 **Calcul de Prime** : Estimation instantanée
- 📊 **Analyse de Risque** : Profil personnalisé
- 🎁 **Recommandations** : Produits adaptés
""")

st.sidebar.markdown("---")
st.sidebar.header("📈 Statistiques")
st.sidebar.metric("Produits Disponibles", len(knowledge_base))
st.sidebar.metric("Questions FAQ", len(faqs))
st.sidebar.metric("Précision", "95%")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

def calculer_prime(type_assurance, age=35, situation="celibataire", fumeur=False, 
                   montant_couverture=100000, duree=20):
    if type_assurance not in knowledge_base:
        return None
    
    prime_base = knowledge_base[type_assurance]["prime_base"]
    
    facteur_age = 1.0
    if age < 25:
        facteur_age = 1.3
    elif age < 40:
        facteur_age = 1.0
    elif age < 60:
        facteur_age = 1.2
    else:
        facteur_age = 1.5
    
    facteur_fumeur = 1.5 if fumeur else 1.0
    
    facteur_situation = 1.0
    if situation == "marie":
        facteur_situation = 0.9
    elif situation == "famille":
        facteur_situation = 0.85
    
    if type_assurance == "assurance_vie":
        facteur_montant = montant_couverture / 100000
        facteur_duree = duree / 20
        prime = prime_base * facteur_age * facteur_fumeur * facteur_montant * facteur_duree
    else:
        prime = prime_base * facteur_age * facteur_fumeur * facteur_situation
    
    return round(prime, 2)

def analyser_risque(age, fumeur, profession, antecedents_medicaux=False, 
                    activites_risque=False):
    score_risque = 0
    facteurs = []
    
    if age < 25:
        score_risque += 30
        facteurs.append("Jeune âge")
    elif age < 40:
        score_risque += 10
        facteurs.append("Âge optimal")
    elif age < 60:
        score_risque += 20
        facteurs.append("Âge moyen")
    else:
        score_risque += 40
        facteurs.append("Âge avancé")
    
    if fumeur:
        score_risque += 30
        facteurs.append("Fumeur")
    
    professions_risque = ["pilote", "pompier", "policier", "militaire", "mineur"]
    if any(p in profession.lower() for p in professions_risque):
        score_risque += 25
        facteurs.append("Profession à risque")
    
    if antecedents_medicaux:
        score_risque += 20
        facteurs.append("Antécédents médicaux")
    
    if activites_risque:
        score_risque += 15
        facteurs.append("Activités à risque")
    
    if score_risque < 30:
        categorie = "Faible"
        emoji = "✅"
        recommandation = "Profil excellent. Primes réduites possibles."
    elif score_risque < 60:
        categorie = "Moyen"
        emoji = "⚠️"
        recommandation = "Profil standard. Primes normales."
    else:
        categorie = "Élevé"
        emoji = "🚨"
        recommandation = "Profil à risque. Surprime probable."
    
    return {
        "score": score_risque,
        "categorie": categorie,
        "emoji": emoji,
        "facteurs": facteurs,
        "recommandation": recommandation
    }

def trouver_reponse(question_user):
    from sklearn.metrics.pairwise import cosine_similarity
    
    question_vector = vectorizer.transform([question_user])
    similarities = cosine_similarity(question_vector, faq_vectors)[0]
    best_match_idx = np.argmax(similarities)
    best_score = similarities[best_match_idx]
    
    if best_score > 0.2:
        return {
            "reponse": faq_reponses[best_match_idx],
            "confiance": float(best_score),
            "question_matched": faq_questions[best_match_idx]
        }
    else:
        return None

tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "💰 Calcul Prime", "📊 Analyse Risque", "🎁 Recommandations"])

with tab1:
    st.subheader("💬 Conversation avec l'Assistant IA")
    
    st.markdown("### 💡 Questions Suggérées")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 Comment calculer ma prime ?"):
            question = "Comment calculer ma prime d'assurance ?"
            st.session_state.chat_history.append({"role": "user", "content": question})
            response = trouver_reponse(question)
            if response:
                st.session_state.chat_history.append({"role": "bot", "content": response['reponse']})
    
    with col2:
        if st.button("📋 Différence assurance vie/décès ?"):
            question = "Quelle est la différence entre assurance vie et décès ?"
            st.session_state.chat_history.append({"role": "user", "content": question})
            response = trouver_reponse(question)
            if response:
                st.session_state.chat_history.append({"role": "bot", "content": response['reponse']})
    
    with col3:
        if st.button("📞 Comment faire un sinistre ?"):
            question = "Comment faire une déclaration de sinistre ?"
            st.session_state.chat_history.append({"role": "user", "content": question})
            response = trouver_reponse(question)
            if response:
                st.session_state.chat_history.append({"role": "bot", "content": response['reponse']})
    
    st.markdown("---")
    
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">👤 Vous : {message["content"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message">🤖 Assistant : {message["content"]}</div>', 
                           unsafe_allow_html=True)
    
    user_input = st.text_input("💬 Posez votre question :", key="user_input", 
                                placeholder="Ex: Combien coûte une assurance vie ?")
    
    col1, col2 = st.columns([1, 5])
    
    with col1:
        send_button = st.button("📤 Envoyer")
    
    with col2:
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.chat_history = []
            st.rerun()
    
    if send_button and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        response = trouver_reponse(user_input)
        
        if response:
            bot_response = f"{response['reponse']}\n\n_(Confiance: {response['confiance']*100:.0f}%)_"
        else:
            bot_response = ("Je n'ai pas trouvé de réponse exacte à votre question. "
                          "Pourriez-vous la reformuler ou utiliser le calculateur de prime ?")
        
        st.session_state.chat_history.append({"role": "bot", "content": bot_response})
        st.rerun()

with tab2:
    st.subheader("💰 Calculateur de Prime d'Assurance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        type_assurance = st.selectbox(
            "📋 Type d'Assurance",
            options=list(knowledge_base.keys()),
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        age = st.slider("🎂 Âge", 18, 80, 35)
        
        situation = st.selectbox(
            "👨‍👩‍👧 Situation Familiale",
            options=["celibataire", "marie", "famille"],
            format_func=lambda x: x.capitalize()
        )
        
        fumeur = st.checkbox("🚬 Fumeur")
    
    with col2:
        st.info(f"**À propos de {type_assurance.replace('_', ' ').title()}**\n\n{knowledge_base[type_assurance]['description']}")
        
        st.write("**Facteurs de tarification :**")
        for facteur in knowledge_base[type_assurance]['facteurs']:
            st.write(f"• {facteur}")
    
    if type_assurance == "assurance_vie":
        col1, col2 = st.columns(2)
        with col1:
            montant_couverture = st.number_input(
                "💵 Montant de Couverture (€)",
                min_value=10000,
                max_value=1000000,
                value=100000,
                step=10000
            )
        with col2:
            duree = st.slider("📅 Durée (années)", 5, 40, 20)
    else:
        montant_couverture = 100000
        duree = 20
    
    if st.button("💰 Calculer la Prime", key="calc_prime"):
        prime = calculer_prime(
            type_assurance,
            age=age,
            situation=situation,
            fumeur=fumeur,
            montant_couverture=montant_couverture,
            duree=duree
        )
        
        st.markdown("---")
        st.success("### 📊 Résultat du Calcul")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Prime Annuelle", f"{prime}€", delta=None)
        
        with col2:
            st.metric("Prime Mensuelle", f"{prime/12:.2f}€", delta=None)
        
        with col3:
            st.metric("Prime Journalière", f"{prime/365:.2f}€", delta=None)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Détails de la Prime")
            st.write(f"• Type: {type_assurance.replace('_', ' ').title()}")
            st.write(f"• Âge: {age} ans")
            st.write(f"• Situation: {situation.capitalize()}")
            st.write(f"• Fumeur: {'Oui' if fumeur else 'Non'}")
            if type_assurance == "assurance_vie":
                st.write(f"• Couverture: {montant_couverture:,}€")
                st.write(f"• Durée: {duree} ans")
        
        with col2:
            st.markdown("### 💡 Conseils")
            if fumeur:
                st.warning("🚭 En arrêtant de fumer, vous pourriez économiser jusqu'à 30% sur votre prime.")
            if age > 50:
                st.info("📊 À votre âge, considérez une assurance vie avec épargne.")
            if situation == "famille":
                st.success("👨‍👩‍👧 Vous bénéficiez d'une réduction famille de 15%.")

with tab3:
    st.subheader("📊 Analyse de Profil de Risque")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age_risque = st.slider("🎂 Âge", 18, 80, 35, key="age_risque")
        fumeur_risque = st.checkbox("🚬 Fumeur", key="fumeur_risque")
        profession = st.text_input("💼 Profession", "Ingénieur", key="profession")
    
    with col2:
        antecedents = st.checkbox("🏥 Antécédents Médicaux", key="antecedents")
        activites_risque = st.checkbox("🏔️ Activités à Risque (sports extrêmes)", key="activites")
    
    if st.button("📊 Analyser mon Profil", key="analyze"):
        risque = analyser_risque(
            age=age_risque,
            fumeur=fumeur_risque,
            profession=profession,
            antecedents_medicaux=antecedents,
            activites_risque=activites_risque
        )
        
        st.markdown("---")
        st.success("### 📈 Résultat de l'Analyse")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Catégorie de Risque", f"{risque['emoji']} {risque['categorie']}")
        
        with col2:
            st.metric("Score de Risque", f"{risque['score']}/100")
        
        with col3:
            progress = risque['score'] / 100
            st.progress(progress)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Facteurs Identifiés")
            for facteur in risque['facteurs']:
                st.write(f"• {facteur}")
        
        with col2:
            st.markdown("### 💡 Recommandation")
            if risque['categorie'] == "Faible":
                st.success(risque['recommandation'])
            elif risque['categorie'] == "Moyen":
                st.warning(risque['recommandation'])
            else:
                st.error(risque['recommandation'])

with tab4:
    st.subheader("🎁 Recommandations Personnalisées")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age_reco = st.slider("🎂 Votre Âge", 18, 80, 35, key="age_reco")
    
    with col2:
        situation_reco = st.selectbox(
            "👨‍👩‍👧 Situation",
            ["celibataire", "marie", "famille"],
            key="situation_reco"
        )
    
    with col3:
        budget = st.number_input("💰 Budget Mensuel (€)", 50, 1000, 150, step=10)
    
    if st.button("🎁 Obtenir mes Recommandations", key="reco"):
        st.markdown("---")
        st.success("### 🎯 Produits Recommandés pour Vous")
        
        for produit_key in knowledge_base.keys():
            prime = calculer_prime(produit_key, age=age_reco, situation=situation_reco)
            prime_mensuelle = prime / 12
            
            if prime_mensuelle <= budget:
                priorite = "Haute" if produit_key in ["assurance_vie", "assurance_habitation"] else "Moyenne"
                
                with st.container():
                    st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"### {produit_key.replace('_', ' ').title()}")
                        st.write(knowledge_base[produit_key]['description'])
                        st.write(f"**Priorité** : {priorite}")
                    
                    with col2:
                        st.metric("Prime/mois", f"{prime_mensuelle:.2f}€")
                        st.metric("Prime/an", f"{prime:.0f}€")
                    
                    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Développé par Maram Chebbi - Data Science & Actuariat")
st.text("Contact: chebbimaram0[at]gmail.com")
