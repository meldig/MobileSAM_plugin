# MobileSAM_plugin

MobileSAM_plugin est une adaptation QGIS du projet [MobileSAM](https://github.com/ChaoningZhang/MobileSAM). Ce plugin vous permet d'utiliser toute la puissance de MobileSAM dans QGIS.

# Fonctionnement

MobileSAM_plugin prend en entrée une couche raster, une couche vecteur et une emprise d'analyse. La couche vecteur contient les prompts nécessaires à la création des masques dans MobileSAM, il peut s'agir soit de points, soit de boîtes englobantes. Pour l'emprise d'analyse, vous pouvez soit définir la votre à partir des coordonnées, soit utiliser le zoom du canvas QGIS.

MobileSAM_plugin produit en sortie une couche vecteur contenant les polygnones recouvrant les objets à vectorisés indiqués dans la couche vecteur (contenant les prompts) et aussi le score des masques générés par le modèle.

À ce jour, seule les scores des masques sont produits, la partie sur la création de la couche vecteur est encore en développement.

# Installation

Pour installer ce plugin il vous suffit de cloner le dépôt, de le zipper et de l'installer dans QGIS en suivant les instructions suivantes : Extensions > Installer/Gérer les extensions > Installer depuis un ZIP. Choisissez ensuite le dossier que vous venez de zipper et cliquez sur Installer le plugin.

Vous aurez accès à ce plugin dans votre boîte à outils : Traitement > Boîte à outils

# Modèle

Vous retrouverez également dans le projet un modèle que vous pouvez utiliser dans le modeleur graphique de QGIS : Traitement > Modeleur Graphique. Appuyez ensuite sur la flèche verte d'exécution du modèle, remplissez le formulaire et cliquez sur exécuter.

Attention, vous devez cependant avoir déjà installer le plugin pour utiliser le modèle !
