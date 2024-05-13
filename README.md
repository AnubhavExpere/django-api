# Playlist Management API

## Overview
The Playlist Management API is designed to manage songs and playlists. It provides endpoints for creating, listing, editing, and deleting songs and playlists.

#       *IMPORTANT: ***Ensure that there is always a trailing slash at the end of the URL when making API requests to receive the expected response.***

### 1. Create New Song
This endpoint adds a new song to the database.

**Endpoint:** `POST /api/songs/`

**Example Request Body:**
```json
{
    "name": "La Vie en Rose",
    "artist": "Edith Piaf",
    "release_year": 1947
}
```
##### Response Status Code: 201 (Success)

### 2. List available songs

This endpoint allows you to retrieve a list of available songs in the app. The response is paginated, with a default limit of 10 songs per page. You can use the `page` query parameter to fetch songs beyond the first 10.

**Endpoint:** `GET /api/songs/`

Example: `GET /api/songs?page=1`

Query Parameters:

- `page` (integer, optional): Get a specific page of results. Defaults to 1 if not provided.
- `q` (string, optional): Search by song name. If a substring of the song name is provided, the matching songs will be included in the response.

##### Response Status Code: 200 (Success)


### 3. Create new playlist

This endpoint can be used to add a new playlist entry in the playlists table.

**Endpoint:** `POST /api/playlists/`

**Example Request Body:**
```json
{
    "name": "Focus",
    "songs": [7, 3, 1, 10]
}
```
##### Response Status Code: 200 (Success)


### 4. List available playlists

This endpoint can be used to list all the available playlists in the app.

**Endpoint:** `GET /api/playlists/`

Example: `GET /api/playlists?page=1`

Query Parameters:
- `page` (integer, optional): Get a specific page of results. Defaults to 1 if not provided.
- `q` (string, optional): Search by song name. If a substring of the song name is provided, the matching songs will be included in the response.

##### Response Status Code: 200 (Success)


### 5. Edit playlist metadata

This endpoint can be used to change the name of an existing playlist.

**Endpoint:** `PUT /api/playlists/<playlist_id>/`

Example: `PUT /api/playlists/3/`

**Example Request Body:**
```json
{
    "name": "Focus - Classics"
}
```
##### Response Status Code: 200 (Success)

### 6. - Delete playlist

This endpoint can be used to delete an existing playlist.

**Endpoint:** `DELETE /api/playlists/<playlist_id>/`

##### Response Status Code: 200 (Success)

### 7. List playlist songs

This endpoint can be used to list all the songs associated with a playlist

**Endpoint:** `GET /api/playlists/<playlist_id>/songs`

Example: `GET /api/playlists/3/songs?page=1`

Query Parameters:
- `page` (int) - Go to a different page of results.

##### Response Status Code: 200 (Success)

### 8. Move playlist song

This endpoint can be used to move a song up and down in a playlist, i.e. reposition it.

**Endpoint:** `PUT /api/playlists/<playlist_id>/songs/<song_id>/`

Example: `PUT /api/playlists/3/songs/7/`

**Example Request Body:**
```json
{
    "position": 4
}
```

##### Response Status Code: 200 (Success)

### 9. Remove playlist song

This endpoint can be used to remove a song from a playlist

**Endpoint:** `DELETE /api/playlists/<playlist_id>/songs/<song_id>/`

Example: `DELETE /api/playlists/3/songs/7/`

**Example Request Body:**
```json
{
    "position": 4
}
```

##### Response Status Code: 200 (Success)
