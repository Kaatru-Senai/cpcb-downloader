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


## ARCHITECTURE

<img src="https://user-images.githubusercontent.com/81956230/203494306-023c97a5-f195-4824-ad06-7b58b358f58f.jpg" width="500px" />


* Everything start with getting request in `/query` endpoint where it takes "from_data", "to_date" and "mail" and initialize Obj from downloader class in `main.py` where it create a thread for the `start_process` (which download the data) and create a unique `id` for that object and send the id to that input email.
* Then it puts this object inside Waiting `Queue` or list.
* To send the progress there is a `websocket` with `/ws` endpoint which takes process id (the unique id created while initialization of downloader obj) and send the estimated time to complete the downloading process and the percentage of download completetion.

* There is a schedular function, in a interval of 5 seconds it checks the `python dictonary` (which contains all the running data download process) if number of process/object inside that dictionary is less than `10` then it pop/dequeue a element from waiting queue and start that process thread, and puts inside dictionary, Also if any process inside dictionary is completed it pop that process from that dict.
* The downloaded data save as csv file wher the file name is the object unique id.
* Api endpoint with ```/get_csv ``` which will take the `file name` or `id` of the process and return the downloaded csv file.
* After one file downloaded a function `clear_directory` will delete all the csv file which are the there for hour or more.



# DOWNLOAD and RUN
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
