# AzCleaner

Function app to scrub an Azure Dev/Test subscription keeping costs down!

- Searches for Resource Groups that don't match string to keep long lived resources around
- Posts to Discord with names of RGs that have been cleaned up
- Uses System assigned Managed Identity for Auth

## Deployment
- run `terraform apply` in `./terraform`
- run `func azure functionapp publish {Function-App-Name}` in `./functionapp`