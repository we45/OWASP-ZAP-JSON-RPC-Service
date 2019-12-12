## OWASP ZAP - JSON RPC Service

### Why?
- I have been working on using OWASP ZAP with NodeJS E2E Testing Frameworks like Nightwatch and Puppeteer (will release code tomorrow),
but I realized that ZAP's JavaScript API is difficult to work with (callback hell and no support for Promises, async/await)
- Given this situation, I figured that it might be useful to create a minimalistic wrapper around ZAP that is "Action-oriented" (hence JSON-RPC). That way, key features of zap can be used without direct access to the API
- This can be extremely useful when using existing functional test automation with ZAP. You don't have to write a whole new API interaction with ZAP. Just call specific functions in this JSON-RPC service and you are off to the races!
- This is a first-ditch attempt at a lightweight and minimalistic JSON-RPC Service for OWASP ZAP

### What's there
- It starts OWASP ZAP from the command line (you need to setup an .env file)
- Launch ZAP Active Scan, Spider, etc
- Generate Report (JSON) to a particular path. You need the ZAP Export Report plugin for this to work.

### TODO
- Context
- Additional AScan, Stats stuff
- Other ZAP Features

### Important!!!
- There's no authentication for the JSON-RPC service. And while it has limited methods. Please use with caution.

### Install and Run
- Install deps from `requirements.txt` => Py3
- create a .env file (like the example `.env` in the repo) in the same directory
- Run the JSON RPC Service with a simple `python ZAPJSONRpc.py`

### Request and Response Examples

#### Start ZAP Scanner (the tool)

POST http://localhost:4000/jsonrpc

```javascript
{
	"method": "start_zap_scanner",
	"jsonrpc": "2.0",
	"id": 0
}

```


#### Start ZAP Active Scan
POST http://localhost:4000/jsonrpc

```javascript
{
	"method": "start_zap_active_scan",
	"params": {
		"baseUrl": "http://localhost:9000",
		"scan_policy": "Light",
		"in_scope_only": true
	},
	"jsonrpc": "2.0",
	"id": 2
}
```

This returns:
```javascript
{
	"result": {
		"scan_id": "0",
		"message": "Scan Successfully Started"
	},
	"id": 3,
	"jsonrpc": "2.0"
}
```
> you need to query scan status with the `scan_id`

#### Get Scan Status
POST http://localhost:4000/jsonrpc

```javascript
{
	"method": "get_ascan_status",
	"params": [0],
	"jsonrpc": "2.0",
	"id": 3
}
```
> `params` here is the `scan_id` from before. You need to encapsulate it in a array object



This returns:
```javascript
{
	"result": "100",
	"id": 3,
	"jsonrpc": "2.0"
}
```
> `result` here is the percentage of scan completion of `scan_id` 0

#### ZAP Shutdown
POST http://localhost:4000/jsonrpc

```javascript
{
	"method": "kill_zap",
	"jsonrpc": "2.0",
	"id": 0
}
```


