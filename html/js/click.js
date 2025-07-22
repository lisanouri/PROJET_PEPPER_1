// Ce script s'exécute quand le document HTML est complètement chargé
$(document).ready(function () {

    // Création d'une session Qi avec le robot Pepper
    session = new QiSession();

    /**
     * Fonction utilitaire qui lève un événement dans ALMemory de Pepper
     * @param {string} event - Le nom de l'événement
     * @param {any} value - La valeur transmise avec l'événement
     */
    function raise(event, value) {
        session.service("ALMemory").done(function(ALMemory) {
            // Lève l'événement dans la mémoire du robot
            ALMemory.raiseEvent(event, value);
        });
    }

    // Lorsqu'on clique sur l'image de "pikachu"
    $('#pikachu').on('click', function() {
        console.log("click pikachu");
        // On lève un événement dans ALMemory, que Pepper peut intercepter dans le dialogue
        raise('SimpleWeb/pikachu', 1)
    });

    $('#bulbizarre').on('click', function() {
        console.log("click bulbizarre");
        raise('SimpleWeb/bulbizarre', 1)
    });

    $('#salameche').on('click', function() {
        console.log("click salameche");
        raise('SimpleWeb/salameche', 1)
    });

    $('#dracaufeu').on('click', function() {
        console.log("click dracaufeu");
        raise('SimpleWeb/dracaufeu', 1)
    });

    $('#onix').on('click', function() {
        console.log("click onix");
        raise('SimpleWeb/onix', 1)
    });

    $('#venusaur').on('click', function() {
        console.log("click venusaur");
        raise('SimpleWeb/venusaur', 1)
    });

    $('#rattata').on('click', function() {
        console.log("click rattata");
        raise('SimpleWeb/rattata', 1)
    });
});
