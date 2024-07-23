<script lang="ts">
	export let url: string;
	export let type: 'website' | 'mastodon' | 'linkedin' | 'github' | 'picture' = 'website';

	const iconMapping = {
		website: 'fas fa-globe',
		mastodon: 'fab fa-mastodon',
		linkedin: 'fab fa-linkedin-in',
		github: 'fab fa-github',
		picture: 'fas fa-camera'
	};
</script>

<a href={url} target="_blank"><i class={iconMapping[type]}></i></a>

<style lang="scss">
	a {
		background-color: #f14a3b;
		color: #fff;
		border-radius: 100%;
		width: 2.5rem;
		padding: 0.5rem 0.2rem;
		text-align: center;
		height: 2.5rem;
		text-decoration: none;
		display: inline-block;
		margin-right: 0.6rem;
	}

	i {
		font-size: 1.5rem;

		&.fa-linkedin-in {
			position: relative;
			left: 0.02rem;
		}

		&.fa-camera {
			position: relative;
			top: -0.05rem;
		}
	}

	a:hover {
		background-color: #fcb70f;
	}
</style>
