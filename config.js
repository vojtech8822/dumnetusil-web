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
    "prodej@dumnetusil.cz",
    "vojtech@havranek.in"
  ],

  // Stránka, na kterou bude uživatel přesměrován po odeslání
  // (prázdné = zůstane na webu)
  thankYouRedirect: ""
};
