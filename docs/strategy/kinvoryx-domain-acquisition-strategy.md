# Kinvoryx Domain Acquisition Strategy

**Status:** Preliminary brand-infrastructure recommendation  
**Version:** 0.1  
**Date:** August 8, 2026

## Executive recommendation

If `kinvoryx.com` remains unregistered and is not classified as a premium domain, acquiring the core Kinvoryx domain portfolio should be inexpensive.

Recommended acquisition order:

1. `kinvoryx.com` — primary and essential
2. `kinvoryx.ai` — defensive registration if Kinvoryx is likely to become the product or company name
3. Defer `.io`, `.co`, `.net`, and other extensions until the brand has stronger commercial traction

The expected initial cost for the `.com` plus a two-year `.ai` registration is approximately **$170**, assuming standard rather than premium pricing.

## Indicative pricing

| Domain | Indicative initial cost | Indicative renewal cost | Recommendation |
|---|---:|---:|---|
| `kinvoryx.com` | Approximately $10–15 | Approximately $12–19 per year | Use as the primary domain |
| `kinvoryx.ai` | Approximately $140–160 for two years | Approximately $100–115 per year, typically billed in a two-year term | Purchase defensively if committed to the brand |
| `kinvoryx.io` | Approximately $35 | Approximately $60–66 per year | Unnecessary if the `.com` is available |
| `kinvoryx.co` | Frequently $10–30 initially | Approximately $30 per year | Defensive purchase only |

Prices vary by registrar, promotion, registry rules, and whether the name is treated as a premium domain.

## Current registrar reference points

At the time of this review, Namecheap listed:

- `.com` registration at **$11.28** and renewal at **$18.48**.
- `.ai` registration at **$159.96** for the required two-year term.
- `.ai` renewal at **$229.96** for two years.
- `.io` registration at approximately **$34.98**, with a substantially higher renewal price.

The first-year promotional price should not drive the decision. Renewal pricing, minimum registration periods, privacy charges, DNS features, and premium-domain renewal terms matter more over the life of the brand.

## Recommended domain architecture

Use:

```text
kinvoryx.com
```

as the canonical company and product domain.

If acquired, configure:

```text
kinvoryx.ai -> kinvoryx.com
```

as a permanent redirect. The `.ai` extension reinforces the technology positioning, but the `.com` is more conventional and credible for a household financial-decision platform.

Potential future subdomains include:

```text
app.kinvoryx.com       Product application
advisors.kinvoryx.com  Advisor experience or marketing
docs.kinvoryx.com      Product and API documentation
research.kinvoryx.com  Research and methodology
status.kinvoryx.com    Service status
```

Avoid purchasing a separate domain for every product lab. A single authoritative domain creates a stronger trust boundary and brand identity.

## Registrar recommendation

Cloudflare Registrar is a strong default because it offers domains at registry cost without renewal markups and includes DNSSEC, WHOIS redaction, DNS, CDN, and SSL capabilities.

Namecheap is also reasonable when its user experience or promotional price is preferable, but renewal costs should be reviewed before purchase.

Regardless of registrar:

- Enable automatic renewal.
- Require multifactor authentication.
- Enable registrar lock and DNSSEC.
- Use an organization-controlled email address for ownership.
- Record the registrant, payment method, renewal dates, and recovery process.
- Do not allow a contractor or individual developer to own the primary domain personally.

## Availability caveat

The absence of a Kinvoryx website or search-engine result does not establish domain availability. Availability must be confirmed through a live registrar search immediately before purchase.

Recommended process:

1. Complete a preliminary trademark and company-name screen.
2. Check `kinvoryx.com` and `kinvoryx.ai` through one reputable registrar.
3. Confirm that neither is subject to premium acquisition or premium renewal pricing.
4. Purchase both in the same session if the brand decision is sufficiently advanced.
5. Do not repeatedly search the name across numerous domain marketplaces before purchasing.

## Brand-risk caveat

Domain availability is not equivalent to legal clearance. Before investing materially in Kinvoryx, conduct:

- USPTO trademark screening
- State business-name screening
- Common-law and internet-use research
- App-store and social-handle checks
- Phonetic and spelling-confusion review

The invented nature of Kinvoryx may improve domain availability and distinctiveness, but it also creates pronunciation and spelling risk. Brand testing should confirm whether prospective users reliably hear, spell, and recall the name.

## Sources

- [Namecheap `.com` pricing](https://www.namecheap.com/domains/registration/gtld/com/)
- [Namecheap `.ai` pricing](https://www.namecheap.com/domains/registration/cctld/ai/)
- [Namecheap `.io` pricing](https://www.namecheap.com/domains/registration/cctld/io/)
- [Cloudflare Registrar](https://www.cloudflare.com/products/registrar/)
- [Cloudflare `.com` registration](https://www.cloudflare.com/application-services/products/registrar/buy-com-domains/)
- [Cloudflare `.ai` registration](https://www.cloudflare.com/application-services/products/registrar/buy-ai-domains/)

## Repository placement

Recommended location:

```text
docs/strategy/kinvoryx-domain-acquisition-strategy.md
```

This belongs in `docs/strategy/` while Kinvoryx remains a working brand. If the repository later develops a broader brand and company-operations section, move it to:

```text
docs/company/brand/kinvoryx-domain-acquisition-strategy.md
```
