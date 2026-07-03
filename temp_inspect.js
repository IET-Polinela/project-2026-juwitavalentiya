const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('http://localhost:8000/login/');
  await page.waitForSelector('form', { timeout: 10000 });
  await page.locator('input[name="username"]').fill('admin');
  await page.locator('input[name="password"]').fill('admin123');
  await page.locator('form').evaluate((form) => form.requestSubmit());
  await page.waitForURL(/\/(dashboard\/)?$/, { timeout: 15000 });
  console.log('after login url', page.url());
  const html = await page.content();
  console.log('contains searchInput', html.includes('searchInput'));
  console.log('contains Manajemen Laporan', html.includes('Manajemen Laporan'));
  console.log(html.slice(0, 4000));
  await browser.close();
})();
