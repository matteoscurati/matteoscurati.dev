<script lang="ts">
  import type { LogoRect, ColorScheme } from "../lib/logos";

  interface Props {
    rects: LogoRect[];
    scheme: ColorScheme;
    eyeIndices: number[];
    buildGroups: number[][];
    size?: number;
    viewBox?: number;
    groupGap?: number;
    innerGap?: number;
  }

  let {
    rects,
    scheme,
    eyeIndices,
    buildGroups,
    size = 128,
    viewBox = 16,
    groupGap = 130,
    innerGap = 25,
  }: Props = $props();

  const filterId = `glow-${scheme.name}`;

  // Semantic delay map — group-based entrance
  const GROUP_GAP = groupGap;
  const INNER_GAP = innerGap;
  const delayMap = new Map<number, number>();
  buildGroups.forEach((group, gi) => {
    group.forEach((ri, ii) => {
      delayMap.set(ri, gi * GROUP_GAP + ii * INNER_GAP);
    });
  });
  function getDelay(i: number): number {
    return delayMap.get(i) ?? i * 40;
  }

  // Total entrance time (last group end + buffer)
  const maxDelay = Math.max(...[...delayMap.values()]);
  const totalTime = maxDelay + 500;

  let prefersReducedMotion = $state(false);
  let blinking = $state(false);
  let entranceDone = $state(false);

  const eyeSet = new Set(eyeIndices);

  $effect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    prefersReducedMotion = mq.matches;

    if (prefersReducedMotion) {
      entranceDone = true;
      return;
    }

    // Mark entrance done
    const entranceTimer = setTimeout(() => {
      entranceDone = true;
    }, totalTime);

    // Blink every ~8s after entrance
    let blinkInterval: ReturnType<typeof setInterval>;
    const blinkStart = setTimeout(() => {
      blinkInterval = setInterval(() => {
        blinking = true;
        setTimeout(() => (blinking = false), 150);
      }, 8000);
    }, totalTime);

    return () => {
      clearTimeout(entranceTimer);
      clearTimeout(blinkStart);
      if (blinkInterval) clearInterval(blinkInterval);
    };
  });
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<svg
  viewBox="0 0 {viewBox} {viewBox}"
  width={size}
  height={size}
  role="img"
  aria-label="pixel logo — {scheme.name}"
  class="pixel-logo"
>
  <defs>
    <filter id={filterId} x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow
        dx="0"
        dy="0"
        stdDeviation="0.6"
        flood-color={scheme.glow}
        flood-opacity="0.55"
      >
        {#if entranceDone && !prefersReducedMotion}
          <animate
            attributeName="stdDeviation"
            values="0.5;0.8;0.5"
            dur="3s"
            repeatCount="indefinite"
          />
          <animate
            attributeName="flood-opacity"
            values="0.4;0.65;0.4"
            dur="3s"
            repeatCount="indefinite"
          />
        {/if}
      </feDropShadow>
    </filter>
  </defs>
  {#each rects as rect, i}
    <rect
      x={rect.x}
      y={rect.y}
      width={rect.w}
      height={rect.h}
      fill={scheme[rect.role]}
      filter="url(#{filterId})"
      class="pixel"
      class:eye={eyeSet.has(i)}
      class:blink={blinking && eyeSet.has(i)}
      class:no-motion={prefersReducedMotion}
      style="--delay: {getDelay(i)}ms"
    />
  {/each}
</svg>

<style>
  .pixel-logo {
    display: block;
  }

  .pixel-logo:hover {
    animation: head-shake 0.4s ease-in-out;
  }

  .pixel {
    opacity: 0;
    transform: scale(0.8);
    transform-origin: center;
    animation: pixel-in 0.4s ease-out forwards;
    animation-delay: var(--delay);
  }

  .pixel.no-motion {
    opacity: 1;
    transform: scale(1);
    animation: none;
  }

  .pixel.eye.blink {
    opacity: 0.15;
    transition: opacity 0.15s ease;
  }

  @keyframes pixel-in {
    from {
      opacity: 0;
      transform: scale(0.8);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }

  @keyframes head-shake {
    0%,
    100% {
      transform: rotate(0deg);
    }
    25% {
      transform: rotate(-3deg);
    }
    75% {
      transform: rotate(3deg);
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .pixel-logo:hover {
      animation: none;
    }
  }
</style>
