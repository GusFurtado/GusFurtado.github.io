// Revela os blocos .animate-box ao rolar e mostra o botão de voltar ao topo.

if ("IntersectionObserver" in window) {
	document.documentElement.classList.add("js");
	const observer = new IntersectionObserver((entries) => {
		for (const entry of entries) {
			if (entry.isIntersecting) {
				entry.target.classList.add("visible");
				observer.unobserve(entry.target);
			}
		}
	}, { rootMargin: "0px 0px -15% 0px" });
	document.querySelectorAll(".animate-box").forEach((box) => observer.observe(box));
}

const gototop = document.querySelector(".gototop");
window.addEventListener("scroll", () => {
	gototop.classList.toggle("active", window.scrollY > 200);
}, { passive: true });
