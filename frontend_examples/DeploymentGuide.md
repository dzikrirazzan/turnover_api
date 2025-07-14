# 🚀 Frontend Deployment Guide

Complete deployment guide for HR Dashboard frontend dengan berbagai platform dan optimizations.

## Production Build & Optimization

### Next.js Configuration
```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  compress: true,
  poweredByHeader: false,
  generateEtags: false,
  
  // Environment variables
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY,
  },

  // Image optimization
  images: {
    domains: ['turnover-api-hd7ze.ondigitalocean.app'],
    formats: ['image/webp', 'image/avif'],
  },

  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://turnover-api-hd7ze.ondigitalocean.app;",
          },
        ],
      },
    ];
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/',
        destination: '/dashboard',
        permanent: false,
      },
    ];
  },

  // Webpack optimizations
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Optimize bundle size
    if (!dev && !isServer) {
      config.optimization.splitChunks = {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            priority: 10,
            reuseExistingChunk: true,
          },
          common: {
            name: 'common',
            minChunks: 2,
            priority: 5,
            reuseExistingChunk: true,
          },
        },
      };
    }

    return config;
  },
};

module.exports = nextConfig;
```

### Environment Configuration
```bash
# .env.production
NEXT_PUBLIC_API_BASE_URL=https://turnover-api-hd7ze.ondigitalocean.app
NEXT_PUBLIC_APP_NAME=SMART-EN HR Dashboard
NEXT_PUBLIC_VERSION=1.0.0
NEXT_PUBLIC_ENVIRONMENT=production

# Analytics (optional)
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
NEXT_PUBLIC_SENTRY_DSN=https://xxxxx@sentry.io/xxxxx

# .env.staging
NEXT_PUBLIC_API_BASE_URL=https://staging-turnover-api.ondigitalocean.app
NEXT_PUBLIC_APP_NAME=SMART-EN HR Dashboard (Staging)
NEXT_PUBLIC_VERSION=1.0.0-staging
NEXT_PUBLIC_ENVIRONMENT=staging
```

### Build Scripts
```json
// package.json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "type-check": "tsc --noEmit",
    "build:analyze": "ANALYZE=true next build",
    "build:staging": "NODE_ENV=production next build",
    "build:production": "NODE_ENV=production next build",
    "export": "next export",
    "deploy:vercel": "vercel --prod",
    "deploy:netlify": "netlify deploy --prod --dir=out",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

## Deployment Platforms

### 1. Vercel Deployment (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy project
vercel

# Production deployment
vercel --prod
```

#### Vercel Configuration
```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "env": {
    "NEXT_PUBLIC_API_BASE_URL": "https://turnover-api-hd7ze.ondigitalocean.app"
  },
  "build": {
    "env": {
      "NODE_ENV": "production"
    }
  },
  "functions": {
    "app/**": {
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Access-Control-Allow-Methods",
          "value": "GET, POST, PUT, DELETE, OPTIONS"
        },
        {
          "key": "Access-Control-Allow-Headers",
          "value": "Content-Type, Authorization"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://turnover-api-hd7ze.ondigitalocean.app/api/:path*"
    }
  ]
}
```

### 2. Netlify Deployment

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Build and deploy
npm run build
npm run export
netlify deploy --dir=out --prod
```

#### Netlify Configuration
```toml
# netlify.toml
[build]
  command = "npm run build && npm run export"
  publish = "out"

[build.environment]
  NODE_ENV = "production"
  NEXT_PUBLIC_API_BASE_URL = "https://turnover-api-hd7ze.ondigitalocean.app"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Content-Security-Policy = "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://turnover-api-hd7ze.ondigitalocean.app;"

[[redirects]]
  from = "/"
  to = "/dashboard"
  status = 302

[[redirects]]
  from = "/api/*"
  to = "https://turnover-api-hd7ze.ondigitalocean.app/api/:splat"
  status = 200

# SPA fallback
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 3. DigitalOcean App Platform

```yaml
# .do/app.yaml
name: hr-dashboard-frontend
services:
- name: web
  source_dir: /
  github:
    repo: your-username/hr-dashboard
    branch: main
  run_command: npm start
  environment_slug: node-js
  instance_count: 1
  instance_size_slug: basic-xxs
  env:
  - key: NODE_ENV
    value: production
  - key: NEXT_PUBLIC_API_BASE_URL
    value: https://turnover-api-hd7ze.ondigitalocean.app
  - key: NEXT_PUBLIC_APP_NAME
    value: SMART-EN HR Dashboard
  routes:
  - path: /
static_sites:
- name: frontend
  source_dir: /
  github:
    repo: your-username/hr-dashboard
    branch: main
  build_command: npm run build && npm run export
  output_dir: out
  env:
  - key: NEXT_PUBLIC_API_BASE_URL
    value: https://turnover-api-hd7ze.ondigitalocean.app
```

### 4. AWS S3 + CloudFront

```bash
# Build static export
npm run build
npm run export

# Install AWS CLI
aws configure

# Sync to S3
aws s3 sync out/ s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

#### CloudFront Configuration
```json
// cloudfront-config.json
{
  "CallerReference": "hr-dashboard-2024",
  "Comment": "HR Dashboard Distribution",
  "DefaultCacheBehavior": {
    "TargetOriginId": "S3-hr-dashboard",
    "ViewerProtocolPolicy": "redirect-to-https",
    "CachePolicyId": "4135ea2d-6df8-44a3-9df3-4b5a84be39ad",
    "Compress": true
  },
  "Origins": {
    "Quantity": 1,
    "Items": [
      {
        "Id": "S3-hr-dashboard",
        "DomainName": "your-bucket-name.s3.amazonaws.com",
        "S3OriginConfig": {
          "OriginAccessIdentity": ""
        }
      }
    ]
  },
  "Enabled": true,
  "PriceClass": "PriceClass_100"
}
```

## CI/CD Pipeline

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy HR Dashboard

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm run test
    
    - name: Run linting
      run: npm run lint
    
    - name: Type check
      run: npm run type-check

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build application
      run: npm run build
      env:
        NEXT_PUBLIC_API_BASE_URL: ${{ secrets.API_BASE_URL }}
        NEXT_PUBLIC_APP_NAME: SMART-EN HR Dashboard
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build-files
        path: .next/

  deploy-staging:
    if: github.ref == 'refs/heads/staging'
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
    - uses: actions/checkout@v3
    
    - name: Download build artifacts
      uses: actions/download-artifact@v3
      with:
        name: build-files
        path: .next/
    
    - name: Deploy to Staging
      run: |
        # Deploy to staging environment
        npx vercel --token ${{ secrets.VERCEL_TOKEN }} --scope ${{ secrets.VERCEL_ORG_ID }}

  deploy-production:
    if: github.ref == 'refs/heads/main'
    needs: build
    runs-on: ubuntu-latest
    environment: production
    steps:
    - uses: actions/checkout@v3
    
    - name: Download build artifacts
      uses: actions/download-artifact@v3
      with:
        name: build-files
        path: .next/
    
    - name: Deploy to Production
      run: |
        # Deploy to production environment
        npx vercel --prod --token ${{ secrets.VERCEL_TOKEN }} --scope ${{ secrets.VERCEL_ORG_ID }}
    
    - name: Notify deployment
      run: |
        # Send notification to Slack/Discord/etc
        echo "Deployment successful!"
```

## Performance Optimization

### Bundle Analysis
```bash
# Install bundle analyzer
npm install --save-dev @next/bundle-analyzer

# Add to next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer(nextConfig);

# Run analysis
ANALYZE=true npm run build
```

### Performance Monitoring
```typescript
// lib/analytics.ts
export const reportWebVitals = (metric: any) => {
  if (process.env.NODE_ENV === 'production') {
    // Send to analytics service
    console.log('Web Vital:', metric);
    
    // Example: Send to Google Analytics
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', metric.name, {
        event_category: 'Web Vitals',
        value: Math.round(metric.name === 'CLS' ? metric.value * 1000 : metric.value),
        event_label: metric.id,
        non_interaction: true,
      });
    }
  }
};

// app/layout.tsx
import { reportWebVitals } from '@/lib/analytics';

export { reportWebVitals };
```

### Image Optimization
```typescript
// components/ui/OptimizedImage.tsx
import Image from 'next/image';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
  priority?: boolean;
}

export const OptimizedImage: React.FC<OptimizedImageProps> = ({
  src,
  alt,
  width = 400,
  height = 300,
  className = '',
  priority = false,
}) => {
  return (
    <Image
      src={src}
      alt={alt}
      width={width}
      height={height}
      className={className}
      priority={priority}
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAIAAoDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAhEAACAQMDBQAAAAAAAAAAAAABAgMABAUGIWGRkqGx0f/EABUBAQEAAAAAAAAAAAAAAAAAAAMF/8QAGhEAAgIDAAAAAAAAAAAAAAAAAAECEgMRkf/aAAwDAQACEQMRAD8AltJagyeH0AthI5xdrLcNM91BF5pX2HaH9bcfaSd1E2VEelI1CYIbGRvM/k9CGqJNpUF8XXLbdTy9nj9+LCG8lNgkRE+4VleDl3XMdxEHN2T+IzltQhYbNr9t9rIzqOJ8VNT8fBn2vgGV9Rh/0LUk6qdvJqWIGLk5eTYk5k5ZqnTLI5BxtTStFntJ2yccJD/a1xJ1+vdXFVPeGqTnFsyNZM4t1IU8kJYNGD2s/nH5H+igjHJUMdnbpyy9Oi9YAMzw8NqRYM2CGNAeJjp5/k/s/j+d1DZpJz3vO/r9"
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    />
  );
};
```

## Security Configuration

### Content Security Policy
```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // Security headers
  response.headers.set('X-DNS-Prefetch-Control', 'on');
  response.headers.set('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload');
  response.headers.set('X-XSS-Protection', '1; mode=block');
  response.headers.set('X-Frame-Options', 'SAMEORIGIN');
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');

  return response;
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
```

## Monitoring & Error Tracking

### Sentry Integration
```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NEXT_PUBLIC_ENVIRONMENT || 'development',
  tracesSampleRate: 1.0,
  beforeSend(event) {
    // Filter out localhost errors in development
    if (event.request?.url?.includes('localhost') && process.env.NODE_ENV === 'development') {
      return null;
    }
    return event;
  },
});

// sentry.server.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NEXT_PUBLIC_ENVIRONMENT || 'development',
  tracesSampleRate: 1.0,
});
```

## Deployment Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] API endpoints tested
- [ ] Build process working
- [ ] Tests passing
- [ ] Security headers configured
- [ ] Performance optimized
- [ ] Error tracking setup

### Post-Deployment
- [ ] Domain configured
- [ ] SSL certificate active
- [ ] CDN configured
- [ ] Monitoring setup
- [ ] Error tracking working
- [ ] Performance metrics collected
- [ ] Backup strategy implemented

### Production Monitoring
```bash
# Health check endpoint
curl -f https://your-domain.com/api/health || exit 1

# Performance monitoring
lighthouse https://your-domain.com --output=json

# Bundle size monitoring
npm run build:analyze
```

## Quick Deployment Commands

```bash
# Vercel (One-command deploy)
npx vercel --prod

# Netlify
npm run build && npm run export && netlify deploy --dir=out --prod

# AWS S3
npm run build && npm run export && aws s3 sync out/ s3://your-bucket --delete

# Docker
docker build -t hr-dashboard .
docker run -p 3000:3000 hr-dashboard
```

Dengan panduan deployment ini, frontend HR Dashboard akan ter-deploy dengan optimal di berbagai platform dengan performa yang maksimal! 🚀✨
