# Budgeteer

## Client
#### Run
```bash
npm run serve
```
#### Deploy
```bash
now --public && now alias budgeteer && now scale budgeteer.now.sh 1 auto
```

## Server
#### Run
```bash
python index.py
```
#### Deploy
```bash
 now --public && now alias budgeteer-server && now rm "server" --safe
```
