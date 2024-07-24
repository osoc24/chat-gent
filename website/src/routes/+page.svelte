<script lang="ts">
	import '../app.css';

	import osocLogo from '$lib/assets/osoc-logo.svg';

	import ghentLogo from '$lib/assets/logo-gent.svg';
	import district09Logo from '$lib/assets/logo-district09.svg';
	import SocialButton from '$lib/components/SocialButton.svelte';
</script>

<svelte:head>
	<meta name="description" content="ChatGent" />
	<meta name="author" content="ChatGent team, Open Summer of Code 2024" />
	<meta
		name="keywords"
		content="ChatGent, Open Summer of Code, osoc24, osoc2024, Ghent, District09"
	/>

	<title>ChatGent project</title>

	<meta property="og:title" content="ChatGent project" />
	<meta property="og:type" content="website" />
	<meta property="og:url" content="https://osoc24.github.io/chat-gent/" />
	<meta property="og:description" content="Making decisions accessible" />
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
									href="https://test-chatgent.streamlit.app/"
									target="_blank">View project</a
								>
								<a
									class="button button--narrow button--alt"
									href="https://github.com/osoc24/chat-gent"
									target="_blank">Contribute</a
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
			<div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-5 col-md-offset-0 col-lg-6">
				<div class="project-image">
					<enhanced:img src="/static/img1.jpg" alt="Endless legal documents" />
				</div>
			</div>
			<div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-6 col-lg-5 col-md-offset-1">
				<h2 class="h4">The project</h2>
				<p>
					Imagine this, you're come back from your holiday and you hear noise outside. You notice
					there are roadworks and want to know more. But you really don't want to go digging through
					endless legal documents. That's where ChatGent comes in.
				</p>
			</div>
		</div>
		<div class="row">
			<div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-6 col-md-offset-0 col-lg-5">
				<p>
					To make the decisions made by the city of <a href="https://stad.gent/">Ghent</a> more accessible
					to everyone, we created ChatGent. ChatGent is a proof of concept for a smart search which combines
					a conventional search with a the concepts of a chat bot. As you can see, the search bar has
					been replaced with a larger box, allowing users to ask questions in natural language. ChatGent
					will then use Natural Language Processing to turn a user's question into a SPARQL query. This
					is done by sending it to the OpenAI API, together with a selection of some of our examples,
					as well as the labels. This will result in a query which can be used to search through the
					city's decisions.
				</p>
			</div>
			<div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-5 col-lg-6 col-md-offset-1">
				<div class="project-image">
					<enhanced:img src="/static/homepage.png" alt="Proposed Homepage" />
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-5 col-md-offset-0 col-lg-6">
				<div class="project-image">
					<enhanced:img src="/static/search.png" alt="Proposed Search Result Page" />
				</div>
			</div>
			<div class="col-xs-12 col-sm-10 col-sm-offset-1 col-md-6 col-lg-5 col-md-offset-1">
				<p>
					Then we actually send the query to the city's SPARQL endpoint. This will return a subset
					of the decisions, which we can use to compile an answer and a summary. This is done by
					using the OpenAI API again to generate a summary of the decisions. This summary is then
					displayed to the user, together with all relevant sources as well as any other relevant
					pages.
				</p>
				<p>
					If you want to take a look at the proof-of-concept we developed, you can find it down
					below. While this is just a proof-of-concept, we believe that this could be a great way to
					make decisions more accessible to everyone.
				</p>
				<div class="button-group">
					<a
						class="button button--narrow"
						href="https://test-chatgent.streamlit.app/"
						target="_blank">View project</a
					>
					<a
						class="button button--narrow button--alt"
						href="https://github.com/osoc24/chat-gent"
						target="_blank">Contribute</a
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
			<iframe src="https://test-chatgent.streamlit.app/?embed=true" title="demo" style="border: 0px"
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
							<a href="https://joannakalisz.be/" target="_blank"
								><enhanced:img
									class="round"
									src="/static/photos/joanna-kalisz.jpg"
									alt="Joanna Kalisz"
								/></a
							>
						</div>
						<div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
							<h4 class="h6">
								<a href="https://joannakalisz.be/" target="_blank">Joanna Kalisz</a>
							</h4>
							<p>Designer</p>
							<div class="social">
								<SocialButton type="linkedin" url="https://www.linkedin.com/in/joanna-j-kalisz/" />
								<SocialButton type="github" url="https://github.com/jane-00" />
								<SocialButton type="website" url="https://joannakalisz.be/" />
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
								/></a
							>
						</div>
						<div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
							<h4 class="h6">
								<a href="https://rlin.eu/" target="_blank">Robin van der Linde</a>
							</h4>
							<p>Developer</p>
							<div class="social">
								<SocialButton type="mastodon" url="https://en.osm.town/@RLin" />
								<SocialButton type="linkedin" url="https://www.linkedin.com/in/RLinEU/" />
								<SocialButton type="github" url="https://github.com/RobinLinde" />
								<SocialButton type="website" url="https://rlin.eu/" />
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
								/></a
							>
						</div>
						<div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
							<h4 class="h6">
								<a href="https://www.linkedin.com/in/dina-boshnaq" target="_blank">Dina Boshnaq</a>
							</h4>
							<p>Developer</p>
							<div class="social">
								<SocialButton type="linkedin" url="https://www.linkedin.com/in/dina-boshnaq" />
								<SocialButton type="github" url="https://github.com/16dina" />
								<SocialButton type="picture" url="https://www.pexels.com/@dina-boshnaq-123876169" />
							</div>
						</div>
					</li>
				</ul>
			</div>
			<div class="col-xs-12 col-sm-6 col-sm-offset-1 col-md-5 col-lg-5 col-lg-offset-2">
				<h3 class="h5">The coach</h3>
				<ul class="team">
					<li class="row middle-xs">
						<div class="col-xs-3">
							<a href="https://www.linkedin.com/in/kyngstudio/" target="_blank"
								><enhanced:img
									class="round"
									src="/static/photos/christophe-leroy.jpg"
									alt="Christophe Leroy"
								/></a
							>
						</div>
						<div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
							<h4 class="h6">
								<a href="https://www.linkedin.com/in/kyngstudio/" target="_blank"
									>Christophe Leroy</a
								>
							</h4>
							<p>Coach</p>
							<div class="social">
								<SocialButton type="linkedin" url="https://www.linkedin.com/in/kyngstudio/" />
							</div>
						</div>
					</li>
				</ul>
				<h3 class="h5">Our partners</h3>
				<ul class="partners">
					<li class="row middle-xs">
						<div class="col-xs-3">
							<a href="https://stad.gent/" target="_blank"
								><img src={ghentLogo} alt="City of Ghent logo" /></a
							>
						</div>
						<div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
							<h4 class="h6">
								<a href="https://stad.gent/" target="_blank">City of Ghent</a>
							</h4>
						</div>
					</li>
					<li class="row middle-xs">
						<div class="col-xs-3">
							<a href="https://district09.gent/" target="_blank"
								><img src={district09Logo} alt="District09 logo" /></a
							>
						</div>
						<div class="col-xs-9 col-md-8 col-lg-8 col-md-offset-1">
							<h4 class="h6">
								<a href="https://district09.gent/" target="_blank">District09</a>
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
					<a href="https://bit.ly/3x1Hnze"><img src={osocLogo} alt="Open Summer of Code logo" /></a>
				</div>
				<div class="col-xs-6 col-sm-8 col-md-9 col-lg-10">
					<p>
						Made with love at
						<a href="https://osoc.be/editions" target="_blank">osoc&nbsp;2024</a>
					</p>
				</div>
			</div>
		</div>
	</footer>
</div>
