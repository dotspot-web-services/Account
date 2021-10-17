import {backendLookup} from '../lookup'

export function apiRegistry(usr, callback){
    backendLookup("POST", "/Registry/reg", callback, {content: usr})
}

export function apiTweetAction(tweetId, action, callback){
    const data = {id: tweetId, action: action}
    backendLookup("POST", "/Registry/login", callback, data)
}

export function apiTweetDetail(tweetId, callback) {
    backendLookup("GET", `/tweets/${tweetId}/`, callback)
}

export function apiTweetFeed(callback, nextUrl) {
    let endpoint =  "/tweets/feed/"
    if (nextUrl !== null && nextUrl !== undefined) {
        endpoint = nextUrl.replace("http://localhost:8000/api", "")
    }
    backendLookup("GET", endpoint, callback)
}


export function apiTweetList(username, callback, nextUrl) {
    let endpoint =  "/tweets/"
    if (username){
        endpoint =  `/tweets/?username=${username}`
    }
    if (nextUrl !== null && nextUrl !== undefined) {
        endpoint = nextUrl.replace("http://localhost:8000/api", "")
    }
    backendLookup("GET", endpoint, callback)
}