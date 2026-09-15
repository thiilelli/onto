# Historique des versions

## [1.0.0] — 2026-09-15

Première publication. Changements par rapport au prototype académique réalisé sous Protégé (novembre 2025, non publié).

### Corrections de modélisation

- **Restrictions de cardinalité passées de `owl:equivalentClass` à `rdfs:subClassOf`.** En équivalence, une restriction devient une *définition* : toute ressource ayant « au plus 100 produits » (donc aussi celles qui n'en ont aucun) était classée `Boutique`, `Produit`, `Client`… Le raisonneur fusionnait ainsi presque toutes les classes.
- **Règle R3 complétée** : la condition « est payée » annoncée dans le commentaire manquait dans le corps de la règle. Ajout de la propriété `estPayeePar` (Commande → Paiement) et de son inverse `regle`, sans lesquelles la condition était inexprimable.
- `CommandePrioritaire`, `CommandeValide` et `ProduitVendable` déclarées sous-classes de `Commande` / `Produit`.
- Classes de haut niveau déclarées disjointes (`owl:AllDisjointClasses`), ainsi que `LivraisonExpress`/`LivraisonStandard` et `PaiementCarte`/`PaiementMainAMain`.
- Individus déclarés distincts (`owl:AllDifferent`) : sans hypothèse du nom unique, une violation de cardinalité faisait *fusionner* deux individus au lieu de signaler une erreur.
- Propriétés génériques (`nom`, `email`, `telephone`, `adresse`, `date`) conservées comme super-propriétés des propriétés spécifiques au lieu de doublons sans domaine.
- Toutes les propriétés d'objet ont désormais une inverse déclarée.
- Prix, montants et pourcentages typés `xsd:decimal` (au lieu de `xsd:float`).
- Préfixes `wd`/`wdt` mal formés (chevrons inclus dans l'URI) et préfixe `untitled-ontology-6` supprimés.

### Renommages

Espace de noms : `http://www.semanticweb.org/micronet/ontologies/2025/11/e-commerce#` → `https://thiilelli.github.io/Onto/ontology#`.
Identifiants en ASCII et lowerCamelCase ; les libellés accentués sont conservés dans `rdfs:label` (fr + en).

| Prototype | Publication | Prototype | Publication |
|---|---|---|---|
| `Catégorie` | `Categorie` | `Entrepôt` | `Entrepot` |
| `AppartientA` / `Assortie` | `appartientA` / `regroupe` | `Concerne` / `EstConcernéPar` | `concerne` / `aPourAvis` |
| `Contient` / `EstDans` | `contient` / `figureDans` | `Ecrit` / `EstEcritPar` | `ecrit` / `estEcritPar` |
| `Effectue` / `EsteffectuéPar` | `effectue` / `estEffectuePar` | `génère` / `EstGénéréePar` | `genere` / `estGenereePar` |
| `Gère` / `EstGéréePar` | `gere` / `estGereePar` | `Passe` / `EstPassé` | `passe` / `estPasseePar` |
| `Vend` / `EstVenduPar` | `vend` / `estVenduPar` | `fournit` / `FournitPar` | `fournit` / `estFourniPar` |
| `Livre` / `LivréPar` | `livre` / `estLivreePar` | `Stocke` / `StockéDans` | `stocke` / `estStockeDans` |
| `associéÀ` / `estAssociéÀ` | `concerneProduit` / `aPourStock` | `estAppliquéParCoupon` | `aPourCoupon` |
| `estConcernéParRemise` | `aPourRemise` | `dateLivraion` | `dateLivraison` |
| `téléphoneServiceCl` | `telephoneServiceClient` | `numéro`, `quantité`, `capacité`, `spécialité` | `numero`, `quantite`, `capacite`, `specialite` |

### Corrections des données de test

- `S01` était associé à deux produits (`P01`, `P03`) : `P03` rattaché à `S03`, qui n'avait aucun produit.
- `S02` était stocké dans deux entrepôts (`E01`, `E02`) : conservé dans `E02` uniquement.
- `Fa02` portait `note = 2` (propriété des avis) au lieu de `numero = 2`.
- `Cat01`–`Cat04` utilisaient `nom` au lieu de `nomCategorie`.
- `r02` renommé `R02` ; emails de fournisseurs débarrassés du préfixe `mailto:`.
- Chronologie rétablie : paiements, factures et livraisons étaient datés avant les commandes (livraison `L02` deux mois avant sa commande).
- `E03` avait une capacité de 5 pour 45 unités stockées : capacité portée à 50.
- `S04` mis à 0 pour illustrer un produit non vendable (règle R2).
- `O01`, `O02` reliées à leurs paiements.

### Ajouts

- Formes SHACL (`shapes/`) : cardinalités en monde fermé, plages de valeurs, formats, cohérence temporelle et capacité des entrepôts.
- Scripts de raisonnement (Pellet), de validation (pySHACL) et d'interrogation (SPARQL).
- Cinq requêtes SPARQL, 17 tests automatisés, intégration continue GitHub Actions.
- Métadonnées de l'ontologie (Dublin Core, VANN, version) et libellés bilingues.
