from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('msmarco-distilbert-base-tas-b')

query_embedding = model.encode('how can i migrate to github actions?')
passage_embedding = model.encode(['Use GitHub Actions Importer to plan and automate your migration to GitHub Actions.\nGitHub Actions Importer offers the ability to extend its built-in mapping.',
                                  'Before starting your migration to GitHub Actions, it would be useful to become familiar with how it works:',
                                  'Learn how to migrate your existing CI/CD workflows to GitHub Actions',
                                  'GitHub Actions Importer has several optional parameters that you can use to customize the migration process.'])

print("Similarity:", util.dot_score(query_embedding, passage_embedding))
