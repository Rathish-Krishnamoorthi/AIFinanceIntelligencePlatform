export const money = (value) => `₹${Number(value || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
export const titleCase = (value = '') => value.toLowerCase().replace(/\b\w/g, (c) => c.toUpperCase());
