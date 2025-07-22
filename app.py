#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qi
import requests

class PokemonModule:
    """
    Module personnalisé pour Pepper permettant de récupérer des informations 
    sur un Pokémon via l'API PokéAPI et de les énoncer vocalement.
    """

    def __init__(self, session):
        """
        Initialise le module avec une session NAOqi et configure le service de synthèse vocale.
        param: session: session active avec le robot Pepper
        """
        print("PokemonModule init")
        self.session = session
        self.tts = self.session.service("ALTextToSpeech")

    def get_pokemon_info(self, name):
        """
        Récupère les informations d'un Pokémon à partir de la PokéAPI, 
        puis utilise le TTS pour annoncer ses types et son poids.

        param: name: nom du Pokémon à rechercher
        """

        url = "https://pokeapi.co/api/v2/pokemon/{}".format(name.lower())
        response = requests.get(url)

        if response.status_code != 200:
            self.tts.say("Je n'ai pas trouvé d'informations sur {}".format(name))
            return

        data = response.json()
        types = [t["type"]["name"] for t in data["types"]]
        type_str = ", ".join(types)
        weight = data["weight"] / 10.0  # poids en hectogrammes, on convertit en kg

        message = "{} est de type {} et pèse environ {} kilogrammes.".format(name.capitalize(), type_str, weight)
        self.tts.say(message)


def main():
    """
    Fonction principale : initialise l'application NAOqi, enregistre le module Pokémon,
    charge le dialogue défini dans un fichier `.top` et lance la conversation.
    """

    # Création de l'application NAOqi (penser à bien changer l'adresse IP du robot Pepper)
    app = qi.Application(url="tcp://10.50.90.104:9559")
    app.start()
    s = app.session
    
    try:
        # Appelle le service ALTabletService pour afficher la page HTML sur la tablette
        tablet = s.service("ALTabletService")
        tablet.loadApplication("pepper_robsa")
        tablet.showWebview()
    except Exception as e:
            print("Erreur avec ALTabletService:", e)
            
    # Création et enregistrement du module personnalisé Pokémon
    my_module = PokemonModule(s)
    s.registerService("Pokemon", my_module)
    
    # Accès aux services de dialogue et de synthèse vocale
    dialog = s.service("ALDialog")
    tts = s.service("ALTextToSpeech")

    # Active la langue française
    dialog.setLanguage("French")

    # Chemin vers le fichier .top (à adapter selon l’emplacement exact sur le robot)
    topic_path = "/data/home/nao/.local/share/PackageManager/apps/pepper_robsa/dialogue_non_ethique.top"  

    # Charge le topic de dialogue
    topic = dialog.loadTopic(topic_path)
    # Active le topic
    dialog.activateTopic(topic)

    # Lance le topic de dialogue
    dialog.subscribe("pokemon_dialog_example")
    tts.say("Je suis prêt à discuter de Pokémon !")  
    
    try:
        # Attend que l'utilisateur appuie sur Entrée pour arrêter
        raw_input("\n Press Enter when finished:")
    finally:
        # Arrêt propre du moteur de dialogue
        dialog.unsubscribe('simple')

        # Désactivation du topic 
        dialog.deactivateTopic(topic)

        # Déchargement du topic pour libérer la mémoire
        dialog.unloadTopic(topic)
        
    # Exécution de l'application
    app.run()
    

if __name__ == "__main__":
    main()
