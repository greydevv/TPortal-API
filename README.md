# TPortal-REST-API

REST API for TPortal, a quantitative player analysis tool based off of their career statistics.

---
## /v1/players


### GET

#### Description
Returns a list of players currently in the database. Supplying no parameters returns every player.

#### Parameters
| Parameter | Type | Description |
|:-|:-|:-|
| limit | integer| limit the number of results returned |
| position | string | the position abbreviations |
| division | integer | 1, 2, or 3 |
| year | integer | athlete's career years (e.g. 1 for Freshman) |
| q | string | search query the 'first', 'last', and 'institution' fields | 

#### Returns
| Type | Description |
|:-|:-|
| JSON | list of players |

#### Response
| Code | Status | Description |
|:-|:-|:-|
| 200 | success | OK |


### POST

#### Description
Inserts the players supplied in the request body.

#### Body
| Type | Description |
|:-|:-|
| JSON | list of players |

#### Returns
| Type | Description |
|:-|:-|
| JSON | list of players |

#### Response
| Code | Status | Description |
|:-|:-|:-|
| 204 | success | OK |
| 409 | error | insertion would case a duplicate player entry (duplicate pids) |


### PUT

#### Description
Updates the players supplied in the request body (by pid).

#### Body
| Type | Description |
|:-|:-|
| JSON | list of players |

#### Response
| Code | Status | Description |
|:-|:-|:-|
| 204 | success | OK |


### DELETE

#### Description
Deletes the players with the pids corresponding to those sent in the request body.

#### Body
| Type | Description |
|:-|:-|
| JSON | list of player ids (pids) |

#### Response
| Code | Status | Description |
|:-|:-|:-|
| 204 | success | OK |

## /v1/players/\<string:pid\>


### GET

#### Description
Gets the player with the pid supplied in the URL.

#### Returns
| Type | Description |
|:-|:-|
| JSON | player |

#### Response
| Code | Status | Description |
|:-|:-|:-|
| 200 | success | OK |
| 404 | error | player was not found |


### DELETE

#### Description
Deletes the player with the pid supplied in the URL.

#### Response
| Code | Status | Description |
|:-|:-|:-|
| 200 | success | OK |
| 404 | error | player was not found  |
