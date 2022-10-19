# CPCB downloader


## OVERVIEW
It download data from CPCB website send the progress report to the user and save localy as csv file with a unique name, It will take around `8-10 minutes` for all the station's data to be downloaded. A user can send request for download a specific csv file by giving the name of the file with request. After one hour of download of a file, it's automatically deleted.


## TECH STACK
* `Python`
* `fastapi`
* `websocket` #from fastapi 
* `cpcb api`
* `threading`
* `asyncio`
## FEATURES/DESCRIPTION
* The `/query` endpoint takes time duration and emailId and create process which will then download data from cpcb, and send the `id` of that process, the downloaded data file name will be same as the id of the process.
* A websocket with `/ws` endpoint take `process_id` parameter and emit the progress and the estimated time to be completion of the downloading process that was requested with a interval of `5 seconds`.
* Each of the csv file have unique name example: `c19a0ee8-4f7c-11ed-a6de-30d04230008c.csv` created with help of python `uuid` library.
* Each downloading process run on a different thread.
* Maximum `10` downloading can happen at a time, and other will be in `ready` state until the schedular function `schedule` start their process. The schedule function also running in a different thread in a infinite while loop with a interval of `5 seconds`.
* Api endpoint with ```/get_csv ``` which will take the `file name` or `id` of the process and return the downloaded csv file.
* After one file downloaded a function `clear_directory` will delete all the csv file which are the there for hour or more.




# CONTRIBUTE
### Step 1: Clone project
You can use github GUI to download the file as zip or you can use below git command

```sh
git clone https://github.com/Kaatru-Senai/cpcb-downloader.git
cd cpcb-downloader
```

### Step 2: Install requirements
Install necessary library with the help of requirements.txt by using below command
```python
pip install -r requirements.txt  (for windows cmd).

or use, 
pip install ->r requirements.txt (gitbash or hyper terminal)
```
* To run the code use
```python
  uvicorn server:app --reload
  ```

### Step 3: Create new branch
Create a new branch to work on the project
```sh
  git checkout -b <Branch name>
```

### Step 4: Commit changes
Add and commit changes 
```sh
  git add <file name>
  git commit -m "<commit message>"
 ```
### Step 5: Create pull request
Push your branch to the origin, and create pull request

```sh
  git push -u origin <branch name>
 ```



## Authors

* **Suvindran**
* **Abhijeet Ranjan**


## License
This project is licensed under the BSD License - see the [LICENSE.md](LICENSE.md) file for details
