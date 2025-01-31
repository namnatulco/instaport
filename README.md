# InstaPort

At the moment, InstaPort is a toy project/PoC.
It is MIT-Licensed.
It may be extended to non-Instagram platforms at some point.

## Requirements

- podman to build containers
- podman compose to put the containers together
- browser with javascript to interact with the UI

## Usage

### WARNING

This project is highly experimental and therefore unstable.
It uses insecure conventions for caching and does not include security checks where needed.
It does not use a web server, but directly runs flask as application server (on port 8000).
Do not run anywhere near a prod- or internet-exposed environment.

### Building

Create `.env.prod.app` and `.env.prod.db`. Nothing currently depends on them, but your compose will complain if they are missing.

Run:

`podman compose build`

### Running

Run `podman compose up -d`.
This creates a container associated with the webapp and a container associated with the database.

Connect to [localhost:8000](http://localhost:8000), you will be redirected to a plain HTML page.

### Usage
Insert the URL to the desired post and hit the button.
The app will scrape (if not cached) the page and interpret the data.
It will try to pre-generate 500-char-limited Mastodon text posts that contain the event info.
If space allows, the app will append as much as possible from the original Instagram post caption (i.e., the text below an image).
This is useful because the current version cannot really understand locations yet.
It is also a best-guess way to guess the title of the event.
Because interpretation of unformatted text is hard, you will be probably be presented with multiple options.
