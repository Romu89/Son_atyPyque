# Son_atyPyque

Ce GitHub est dédié au projet de Détection de Son Anormal pour le Jul_Bootcamp_DS.

Membres de l'équipe : Francis Bontron, Nicolas Lecointre et Romuald Nguenga.

# Contexte 
D’un point de vue technique :

Il serait avantageux de pouvoir monitorer de manière continue des machines industrielles, et
de pouvoir détecter lorsqu’elles sont défaillantes. En effet sur des chaînes de productions
cela peut éviter des accidents et limiter les pertes dues à des interruptions de la production.
L’approche étudiée dans ce rapport s’inspire de l’ouvrier mécanicien qui connaît parfaitement les
machines sur lesquelles il travaille et qui est capable de détecter des pannes seulement à partir
du bruit qu’elles émettent.

La détection des sons anormaux des machines industrielles rentre dans le cadre de la
maintenance prédictive. L’objectif étant la collecte des données en temps réel au moyen de
capteurs et l’analyse au travers des algorithmes de machine learning afin d'anticiper
d’éventuels dysfonctionnements de la machine.
La détection par l’analyse du son est un moyen simple et peu onéreux de monitorer le bon
fonctionnement d’une usine. Cela demande une certaine robustesse de la part du système,
afin de ne pas interrompre la production pour des fausses alertes, ce qui se révélerait
contre-productif. Mais avec un algorithme qui retourne peu de faux positifs on possède un
moyen sûr et qui demande peu d’investissement pour assurer la sécurité de l’usine.

De manière plus générale, les outils de deep learning et de machine learning se placent
comme des atouts pour l'industrie, mais peinent à percer. Selon le rapport du ministère de
l’économie, Intelligence artificielle - État de l’art et perspectives pour la France, “À l’heure
actuelle, on assiste à un essor des data science utilisées à des fins d’optimisation de
procédés. La dimension cognitive (apprentissage, décision) est encore peu présente dans
ces développements. L’activité industrielle est soumise à des exigences fortes de fiabilité”.
Or l’apport du sujet qui nous intéresse est justement de permettre un gain de fiabilité grâce à la
dimension cognitive, ce qui faciliterait son acceptation.


D’un point de vue économique :

Selon l’Association Française des Ingénieurs et Responsables de Maintenance (AFIM), les
coûts de la maintenance industrielle représentent à peu près 22 milliards d’euros par an en
France. Ce montant élevé est dû principalement aux travaux de maintenance d’urgence qui
nécessitent l’immobilisation des machines de production/fabrication.
Ainsi, pour réduire significativement ce chiffre, il est primordial que les entreprises, qu'elles
soient de petites, moyennes ou grandes tailles, fassent appel à une nouvelle forme de
maintenance, la maintenance prédictive. La force de la maintenance prédictive résidant
dans l’anticipation des pannes, elle permettra aux entreprises d’éviter tout arrêt coûteux de
la chaîne de production (à titre d’illustration, un arrêt de ligne de production chez Renault
leur fait perdre environ 1 million d’euros par jour) et leur permettra de faire des économies
non négligeables. Selon une étude du cabinet McKinsey, la maintenance prédictive
permettra aux entreprises d’économiser 630 milliards de dollars d’ici 2025.


D’un point de vue scientifique :

L’analyse sonore à l’aide d’algorithmes de Deep Learning est une discipline encore très
jeune. En 2018, Google parvient à isoler une voix au milieu de sons ambiants, ou encore à
séparer les voix de deux personnes parlant en même temps pour n’entendre que la
personne désirée. Avec la multiplication des “assistants virtuels” (Alexa, Siri, Google Home,
etc...) la détection de voix est un enjeu important pour les développeurs de ces applications.
Ces méthodes pourraient aussi se coupler aux systèmes de reconnaissance faciale pour ce
qui est de la recherche en sécurité, ou encore à fournir des outils toujours plus performants
dans le domaine de la musique, ou dans la gestion de l'acoustique.
De façon générale, il est important de comprendre les mécanismes entre la production et la
compréhension d’un son.

# Objectifs du projet 

La problématique de ce projet consiste à détecter des anomalies sur des machines à partir
d’un dataset ne contenant que des extraits en fonctionnement nominal. Sa résolution se
décompose en trois grand objectifs :

● Traiter les extraits sonores pour les convertir en des données qu’un réseau de
neurones peut utiliser.

● Développer plusieurs modèles avec différentes stratégies d’apprentissage afin
d’évaluer la capacité à détecter des sons anormaux dans un set de test.

● Comparer les approches, aussi bien dans leurs résultats, la difficulté à les mettre en
place, la rapidité d’exécution, etc...





