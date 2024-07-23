# ChatGent Project Description Website

This folder contains the source code for the ChatGent project description website. The website is a simple static website that gives some information about the project and the team behind it.

The website is deployed over on [https://osoc24.github.io/chat-gent](https://osoc24.github.io/chat-gent).

## How to run

First install the dependencies:

```bash
npm install
```

Then run the development server:

```bash
npm run dev
```

The website will be available at [http://localhost:5173](http://localhost:5173).

## How to deploy

The website is automatically deployed to [GitHub Pages](https://osoc24.github.io/chat-gent) using GitHub Actions. To manually test the deployment, run:

```bash
npm run build
npm run preview
```

This will build the website and serve it locally at [http://localhost:5173](http://localhost:5173).
