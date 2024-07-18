<script lang="ts">
    import "../app.css";

    import osocLogo from "$lib/assets/osoc-logo.svg";

    import ghentLogo from "$lib/assets/logo-gent.svg";
    import district09Logo from "$lib/assets/logo-district09.svg";
</script>

<svelte:head>
    <meta name="description" content="ChatGent"/>
</svelte:head>

<div class="layout">
    <div class="hero">
      <div class="container container-fluid">
        <div class="row around-xs">
          <div class="col-xs-12 col-sm-11 col-md-10 col-lg-9">
            <div class="row hero-card">
              <div class="col-xs-12 col-sm-10 col-md-7 col-lg-8">
                <h1 class="h1 hero-title">ChatGent Project</h1>
              </div>
              <div class="col-xs-12 col-sm-8 col-md-7 col-lg-7">
                <p class="hero-intro">Making decisions accessible</p>
              </div>
              <div class="col-xs-12 col-sm-10 col-md-7 col-lg-8">
                <div class="button-group">
                  <a
                    class="button button--narrow"
                    href="#"
                    target="_blank"
                    >View project</a
                  >
                  <a
                    class="button button--narrow button--alt"
                    href="https://github.com/osoc24/chat-gent"
                    target="_blank"
                    >Contribute</a
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- container -->
    </div>
    <!-- hero -->

    <div class="container container-fluid project-section">
      <div class="row">
        <div
          class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-5 col-md-offset-0 col-lg-6"
        >
          <div class="project-image">
            Image goes here
          </div>
        </div>
        <div
          class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-6 col-lg-5 col-md-offset-1"
        >
          <h2 class="h4">The project</h2>
          <p>
            To make the decisions made by the city of <a href="https://stad.gent/">Ghent</a> more accessible to
            everyone, we created ChatGent. ChatGent is a proof of concept for a
            smart search which combines a conventional search with a the concepts
            of a chat bot.
          </p>
        </div>
      </div>
      <div class="row">
        <div
          class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-6 col-md-offset-0 col-lg-5"
        >
          <p>
            Text
          </p> 
        </div>
        <div
          class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-5 col-lg-6 col-md-offset-1"
        >
          <div class="project-image">
            Space for second image
          </div>
        </div>
      </div>
      <div class="row">
        <div
          class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-5 col-md-offset-0 col-lg-6"
        >
          <div class="project-image">
            Space for third image
          </div>
        </div>
        <div
          class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-6 col-lg-5 col-md-offset-1"
        >
          <p>
            Text
          </p>
          <div class="button-group">
            <a
              class="button button--narrow"
              href="#"
              target="_blank"
              >View project</a
            >
            <a
              class="button button--narrow button--alt"
              href="https://github.com/osoc24/chat-gent"
              target="_blank"
              >Contribute</a
            >
          </div>
        </div>
      </div>
    </div>

    <div class="row center-xs">
      <div class="col-xs-10">
        <h2 class="h4">Demo</h2>
      </div>
      <div class="col-xs-10 project-image">
        <iframe
          src="#"
          title="demo"
          style="border: 0px"
        ></iframe>
      </div>
    </div>

    <div class="container container-fluid project-section">
      <hr />

      <div class="row">
        <div class="col-xs-12 col-sm-5 col-md-6 col-lg-5">
          <h3 class="h5">The team</h3>
          <ul class="team">
            <li class="row middle-xs">
              <div class="col-xs-3">
                <a href="https://www.linkedin.com/in/joanna-j-kalisz/" target="_blank"
                  ><enhanced:img
                    class="round"
                    src="/static/photos/joanna-kalisz.jpg"
                    alt="Joanna Kalisz"
                /></a>
              </div>
              <div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
                <h4 class="h6">
                  <a href="https://www.linkedin.com/in/joanna-j-kalisz/" target="_blank"
                    >Joanna Kalisz</a
                  >
                </h4>
                <p>Designer</p>
                <div class="social">
                  <a
                    href="https://www.linkedin.com/in/joanna-j-kalisz/"
                    target="_blank"
                    ><i class="fab fa-linkedin-in"></i></a
                  ><a href="https://github.com/jane-00" target="_blank"
                    ><i class="fab fa-github"></i
                  ></a>
                </div>
              </div>
            </li>
            <li class="row middle-xs">
              <div class="col-xs-3">
                <a href="https://rlin.eu/" target="_blank"
                  ><enhanced:img
                    class="round"
                    src="/static/photos/robin-van-der-linde.jpg"
                    alt="Robin van der Linde"
                /></a>
              </div>
              <div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
                <h4 class="h6">
                  <a href="https://rlin.eu/" target="_blank"
                    >Robin van der Linde</a
                  >
                </h4>
                <p>Developer</p>
                <div class="social">
                    <a href="https://en.osm.town/@RLin" target="_blank"
                      ><i class="fab fa-mastodon"></i
                    ></a>
                    <a
                      href="https://www.linkedin.com/in/RLinEU/"
                      target="_blank"
                      ><i class="fab fa-linkedin-in"></i></a
                    ><a href="https://github.com/RobinLinde" target="_blank"
                      ><i class="fab fa-github"></i
                    ></a>
                    <a href="https://rlin.eu/" target="_blank">
                      <i class="fas fa-globe"></i
                    ></a>
                  </div>
              </div>
            </li>
            <li class="row middle-xs">
              <div class="col-xs-3">
                <a href="https://www.linkedin.com/in/dina-boshnaq" target="_blank"
                  ><enhanced:img
                    class="round"
                    src="/static/photos/dina-boshnaq.jpg"
                    alt="Dina Boshnaq"
                /></a>
              </div>
              <div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
                <h4 class="h6">
                  <a href="https://www.linkedin.com/in/dina-boshnaq" target="_blank"
                    >Dina Boshnaq</a
                  >
                </h4>
                <p>Developer</p>
                <div class="social">
                  <a
                    href="https://www.linkedin.com/in/dina-boshnaq"
                    target="_blank"
                    ><i class="fab fa-linkedin-in"></i
                  ></a>
                  <a href="https://github.com/16dina" target="_blank"
                    ><i class="fab fa-github"></i>
                  </a>
                  <a href="https://www.pexels.com/@dina-boshnaq-123876169" target="_blank"
                    ><i class="fas fa-camera"></i>
                  </a>
                </div>
              </div>
            </li>
          </ul>
        </div>
        <div
          class="col-xs-12 col-sm-6 col-sm-offset-1 col-md-5 col-lg-5 col-lg-offset-2"
        >
          <h3 class="h5">The coaches</h3>
          <ul class="team">
            <li class="row middle-xs">
              <div class="col-xs-3">
                <a
                  href="https://www.linkedin.com/in/kyngstudio/"
                  target="_blank"
                  ><enhanced:img
                    class="round"
                    src="/static/photos/christophe-leroy.jpg"
                    alt="Christophe Leroy"
                /></a>
              </div>
              <div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
                <h4 class="h6">
                  <a
                    href="https://www.linkedin.com/in/kyngstudio/"
                    target="_blank"
                    >Cristophe Leroy</a
                  >
                </h4>
                <p>Coach</p>
                <div class="social">
                  <a
                    href="https://www.linkedin.com/in/kyngstudio/"
                    target="_blank"
                    ><i class="fab fa-linkedin-in"></i
                  ></a>
                </div>
              </div>
            </li>
          </ul>
          <h3 class="h5">Our partners</h3>
          <ul class="partners">
            <li class="row middle-xs">
              <div class="col-xs-3">
                <a href="https://stad.gent/" target="_blank"
                  ><img src={ghentLogo} alt="City of Ghent logo"
                /></a>
              </div>
              <div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
                <h4 class="h6">
                  <a href="https://stad.gent/" target="_blank"
                    >City of Ghent</a
                  >
                </h4>
              </div>
            </li>
            <li class="row middle-xs">
              <div class="col-xs-3">
                <a href="https://district09.gent/" target="_blank"
                  ><img
                    src={district09Logo}
                    alt="District09 logo"
                /></a>
              </div>
              <div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
                <h4 class="h6">
                  <a href="https://district09.gent/" target="_blank"
                    >District09</a
                  >
                </h4>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <footer>
      <div class="container container-fluid">
        <div class="row middle-xs">
          <div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">
            <a href="https://bit.ly/3x1Hnze"
              ><img src={osocLogo} alt="Open Summer of Code logo"
            /></a>
          </div>
          <div class="col-xs-6 col-sm-8 col-md-9 col-lg-10">
            <p>
              Made with love at
              <a href="https://osoc.be/editions/2024" target="_blank"
                >osoc&nbsp;2024</a
              >
            </p>
          </div>
        </div>
      </div>
    </footer>
  </div>
