/*
 * ========================================
 *  Dům Netušil — konfigurace webu
 * ========================================
 *
 *  Emaily pro kontaktní formulář:
 *  - první email = hlavní příjemce
 *  - další emaily = kopie (CC)
 *
 *  Pro přidání dalšího příjemce stačí přidat
 *  řádek do pole formEmails.
 */

const SITE_CONFIG = {
  formEmails: [
    "vojtech@havranek.in",
    "prodej@dumnetusil.cz"
  ],

  // Stránka, na kterou bude uživatel přesměrován po odeslání
  // (prázdné = zůstane na webu)
  thankYouRedirect: "https://vojtech8822.github.io/dumnetusil-web/?sent=1"
};
