module.exports = {
	plugins: ["@trivago/prettier-plugin-sort-imports"],
	importOrder: ["^[a-z]", "^@", "^[.]", "^[..]"],
	importOrderSortSpecifiers: true, // <-- trie dans les accolades
};
