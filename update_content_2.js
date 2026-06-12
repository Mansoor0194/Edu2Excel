const fs = require('fs');
const cheerio = require('cheerio');

const mapping = {
  "travel-and-tourism": {
    "title": "Travel and Tourism",
    "breadcrumb": "Travel and Tourism",
    "main_text": "EDU2EXCEL primarily focuses on education and immigration services. While they may not offer direct travel and tourism services, their expertise in international education and cultural exchange can be beneficial for those planning to travel for study or other academic purposes.",
    "list_items": [
      "Destination Guidance: They can provide information on popular study destinations, cultural attractions, and cost of living.",
      "Accommodation Assistance: EDU2EXCEL may be able to help you find suitable accommodation options, such as student housing or shared apartments.",
      "Travel Tips: They can offer advice on travel arrangements, transportation, and safety tips for international students.",
      "Cultural Orientation: EDU2EXCEL can provide insights into the local culture, customs, and etiquette to help you adapt to your new environment."
    ],
    "why_choose_title": "WHY CHOOSE EDU2EXCEL",
    "why_choose_subtitle": "Benefits of Choosing EDU2EXCEL",
    "why_choose_text": "While EDU2EXCEL may not offer comprehensive travel and tourism packages, their expertise in international education can be a valuable resource for students planning to travel for academic purposes.<br><br>Would you like to know more about EDU2EXCEL's services or have any specific questions about travel and tourism related to education?"
  }
};

async function run() {
  for (const [folder, data] of Object.entries(mapping)) {
    const filePath = `services/${folder}/index.html`;
    if (!fs.existsSync(filePath)) {
      console.log(`Skipping ${filePath}, does not exist.`);
      continue;
    }
    const html = fs.readFileSync(filePath, 'utf8');
    const $ = cheerio.load(html, { decodeEntities: false });

    // Update <title>
    const titleEl = $('title');
    if (titleEl.length > 0) {
      titleEl.text(`${data.title} - EDU2EXCEL`);
    }

    // Update h1 elementor-heading-title
    const h1 = $('h1.elementor-heading-title');
    if (h1.length > 0) {
      h1.text(data.title);
    }

    $('li').each((i, el) => {
      const text = $(el).text().trim().toLowerCase();
      if (['Travel and Tourism'].includes(text)) {
        $(el).text(data.breadcrumb);
      }
    });

    const mainTextContainer = $('[data-id="366aed4"] .elementor-widget-container');
    if (mainTextContainer.length > 0) {
      mainTextContainer.html(`<p>${data.main_text}</p>`);
    }

    const listContainer = $('[data-id="7fe3374"] ul.elementor-icon-list-items');
    if (listContainer.length > 0) {
      const firstItemHTML = listContainer.find('li').first().html();
      listContainer.empty();
      
      data.list_items.forEach(itemText => {
        const newLi = $('<li class="elementor-icon-list-item"></li>');
        newLi.html(firstItemHTML);
        newLi.find('.elementor-icon-list-text').text(itemText);
        listContainer.append(newLi);
      });
    }

    const whyChooseH3 = $('[data-id="983726c"] h3');
    if (whyChooseH3.length > 0) {
      whyChooseH3.text(data.why_choose_title);
    }

    const whyChooseSubH2 = $('[data-id="bfce2f7"] h2');
    if (whyChooseSubH2.length > 0) {
      whyChooseSubH2.text(data.why_choose_subtitle);
    }

    const whyChooseTextContainer = $('[data-id="95958fa"] .elementor-widget-container');
    if (whyChooseTextContainer.length > 0) {
      whyChooseTextContainer.html(`<p>${data.why_choose_text}</p>`);
    }

    fs.writeFileSync(filePath, $.html());
    console.log(`Updated ${filePath}`);
  }
}

run();
