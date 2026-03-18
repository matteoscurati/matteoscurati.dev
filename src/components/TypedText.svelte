<script lang="ts">
  let { text = "", delayMs = 0, charSpeed = 60 } = $props<{
    text: string;
    delayMs?: number;
    charSpeed?: number;
  }>();

  let displayed = $state("");
  let done = $state(false);
  let started = $state(false);

  $effect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (mq.matches) {
      displayed = text;
      done = true;
      started = true;
      return;
    }

    const startTimer = setTimeout(() => {
      started = true;
      let i = 0;
      const interval = setInterval(() => {
        if (i < text.length) {
          displayed = text.slice(0, i + 1);
          i++;
        } else {
          done = true;
          clearInterval(interval);
        }
      }, charSpeed);

      return () => clearInterval(interval);
    }, delayMs);

    return () => clearTimeout(startTimer);
  });
</script>

<span class="typed-text" aria-label={text}>
  {#if started}
    <span aria-hidden="true">{displayed}</span>{#if !done}<span class="cursor" aria-hidden="true">_</span>{/if}
  {/if}
</span>

<style>
  .typed-text {
    display: inline;
  }

  .cursor {
    animation: blink 0.8s step-end infinite;
    color: var(--color-accent);
  }

  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
  }
</style>
