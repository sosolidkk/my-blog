let didScroll;

$(window).scroll(() => {
  didScroll = true;
});

setInterval(() => {
  if (didScroll) {
    didScroll = false;
    enableBackToTopBtn();
  }
}, 250);

scrollBackTop = () => { $(document).scrollTop(0); canEnable(false); }

enableBackToTopBtn = () => {
  ($(document).scrollTop() > 500) ? canEnable(true) : canEnable(false);
}

canEnable = (condition) => {
  (condition) ? $(".btnTop").css("display", "block") : $(".btnTop").css("display", "none");
}