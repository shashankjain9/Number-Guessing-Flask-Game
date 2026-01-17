// Simple confetti effect when player wins
function launchConfetti() {
    const duration = 3 * 1000;
    const animationEnd = Date.now() + duration;
    const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

    function randomInRange(min, max) {
        return Math.random() * (max - min) + min;
    }

    const interval = setInterval(function() {
        const timeLeft = animationEnd - Date.now();

        if (timeLeft <= 0) return clearInterval(interval);

        confetti({
            particleCount: 3,
            startVelocity: randomInRange(20, 40),
            spread: 360,
            origin: { x: Math.random(), y: Math.random() - 0.2 }
        });
    }, 250);
}
