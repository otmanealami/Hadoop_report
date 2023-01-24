## TP #2 - Hadoop map-reduce.


## Partie I - Anagramme

Dans cette première partie, nous avons développé un script  qui reconnaît les mots contenant les mêmes lettres (mais dans des ordres différents) à partir d un fichier Word. Nous avons  Hadoop pour traiter un fichier de mots en parallèle et utilise un mappeur pour générer une valeur clé pour chaque mot du fichier. 



##  Préparation de l'environnement de deploiement (Hadoop)

Suite à l'installation de docker et des différents s contenaires représentant respectivement un nœud maître (le Namenode) et deux nœuds esclaves (les Datanodes).Cela prend l'architecture suivante

![architecture](hadoop-cluster-docker.png)

```
docker run -itd --net=hadoop -p 9870:9870 -p 8088:8088 -p 7077:7077 \
  -p 16010:16010 -p 9999:9999 --name hadoop-master --hostname hadoop-master \
  stephanederrode/docker-cluster-hadoop-spark-python-16:3.2

```
```
docker run -itd -p 8040:8042 --net=hadoop --name hadoop-slave1 --hostname hadoop-slave1 \
  stephanederrode/docker-cluster-hadoop-spark-python-16:3.2

```
```
docker run -itd -p 8041:8042 --net=hadoop --name hadoop-slave2 --hostname hadoop-slave2 \
  stephanederrode/docker-cluster-hadoop-spark-python-16:3.2

```
Le cluster est déployé comme suit :
```
docker exec -it hadoop-master bash
```

```
./start-hadoop.sh
```
```
mkdir anagramme
cd anagramme
```
Téléchargement du fichier text depuit github

```
wget https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
```

###  Script mapper.py

Le script utilise ensuite une boucle for pour itérer sur chaque mot de la variable "line", qui est divisée en une liste de mots à l'aide de la fonction "split()". Le script applique ensuite les fonctions "join()" et "sorted()" à chaque mot de la liste.

La fonction "join()" est utilisée pour concaténer tous les caractères d'un mot, tandis que la fonction "sorted()" est utilisée pour trier les caractères d'un mot par ordre alphabétique. Le script renvoie ensuite un tuple contenant le mot trié et le mot original.

Le script appelle ensuite la fonction map en passant le sys.stdin comme argument et imprime la sortie. Le sys.stdin renvoie l'entrée de l'utilisateur, qui est passée comme argument à la fonction map.

le script trie les caractères de chaque mot transmis en entrée et renvoie un tuple contenant le mot trié et le mot original, transmis en entrée par l'utilisateur.


###  Script reducer.py

Le script définit une fonction appelée "recude_dic" qui prend un dictionnaire en entrée. Cette fonction itère ensuite sur le dictionnaire, où chaque clé correspond à un groupe de valeurs. La fonction utilise ensuite une instruction if pour vérifier si la longueur des valeurs est supérieure à un. Si c'est le cas, la fonction joint les valeurs du groupe à l'aide du séparateur "\t" et de la fonction "join()", puis mappe les valeurs en chaînes de caractères à l'aide de la fonction "map()".

Le script utilise ensuite une boucle for pour itérer sur l'entrée de sys.stdin, qui est passée comme argument au script. Pour chaque entrée, le script utilise les fonctions "strip()" et "split()" pour supprimer tout espace blanc supplémentaire et diviser l'entrée en une clé et une valeur. Le script ajoute ensuite la valeur à la clé correspondante dans le dictionnaire par défaut. la fonction "recude_dic", en passant le dictionnaire par défaut comme argument. Cela amène la fonction à itérer sur le dictionnaire et à imprimer les valeurs groupées si la longueur du groupe est supérieure à un.

En résumé, ce script regroupe les valeurs en fonction d'une clé, puis imprime les valeurs groupées si la longueur du groupe est supérieure à un. L'entrée est transmise par l'utilisateur via sys.stdin, qui est transmis comme argument au script.


### 1.4 Exsécution des script

Envoi des fichiers mapper et reducer sur l'environnemt de travail :
```
docker cp mapper.py hadoop-master:/root/anagramme
```
```
docker cp reducer.py hadoop-master:/root/anagramme
```
rendre les fichier éxécutable
```
chmod +x mapper.py
chmod +x reducer.py
```
Lancement du job
hadoop jar $STREAMINGJAR -files mapper.py,reducer.py \
  -mapper mapper.py -reducer reducer.py \
  -input input/dracula -output sortie
"""

Récupération du résultat

```
hadoop fs -get sortie/part-00000 output
```

Téléchargement du fichier output 
```

docker cp  hadoop-master:/root/output anagramme/ 
```
dans notre cas le fichier output est stocké anagramme/

## Partie II - Requette relative au fichier de vente sales_query.py

Ce script définit un travail MapReduce qui prend un fichier de données d'achat et produit la ville, le mode de paiement et le montant total des achats de la méthode qui a généré le plus grand profit pour chaque ville.

Il définit d'abord la méthode "steps", qui spécifie les étapes par lesquelles le job va passer. La méthode "steps" renvoie une liste d'objets MRStep, qui sont les étapes individuelles que le job va suivre. Dans ce cas, il y a deux objets MRStep : un qui exécute les fonctions "map_cities" et "profit_by_city_by_method", et un qui exécute les fonctions "remap_function" et "best_purchased_methods".

La fonction "map_cities" est la première fonction mappeur qui est appelée. Elle prend une ligne d'un fichier d'entrée et la nettoie en supprimant tout espace en début ou en fin de ligne, puis en divisant la ligne en une liste de valeurs en utilisant le caractère de tabulation ('\t') comme délimiteur. Il produit ensuite un tuple de la forme (ville, méthode de paiement), ainsi que le montant de l'achat. Cela crée une paire clé-valeur où la clé est la ville et le mode de paiement et la valeur est le montant de l'achat.

La fonction "profit_by_city_by_method" est la première fonction réductrice appelée. Elle reprend les paires clé-valeur produites par la fonction "map_cities", où la clé est un tuple de la forme (ville, mode de paiement), et les valeurs sont les montants des achats. La fonction additionne les montants des achats pour chaque clé et produit la clé et le montant total des achats comme valeur.

La "remap_function" est la deuxième fonction de mappage appelée. Elle prend les paires clé-valeur produites par la fonction "profit_by_city_by_method" et les remappe de sorte que la clé soit la ville et la valeur un tuple de la forme (payment_method, total_purchase_amount).

Enfin, la fonction "best_purchased_methods" est la deuxième fonction réductrice appelée. Elle prend les paires clé-valeur produites par la fonction "remap_function", où la clé est la ville et les valeurs sont des tuples de la forme (payment_method, total_purchase_amount). La fonction itère à travers les tuples et garde la trace de la méthode de paiement avec le montant total d'achat le plus élevé, et elle donne la ville, la méthode de paiement, et le montant total d'achat.


rendre le fichier éxécutable
```
chmod +x sales_query.py
```
Lancement de job ( sous réserve de stockage seul un fichier de 100 lignes  purchases_extrait100.txt figure dans la directory)
vente/ à travers la commande cat purchases.txt | head -n 100 > purchases_extrait100.txt

```
python3 sales_query.py purchases.txt -r hadoop > output_file.txt
```

Récupération du fichier output_file.txt
```

docker cp  hadoop-master:/root/ventes/output.txt ventes/ 

```