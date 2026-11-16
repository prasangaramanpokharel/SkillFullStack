#!/usr/bin/env python3
"""
scaffoldGoModule.py
Scaffolds an idiomatic Go service layout with cmd/server/main.go, internal/platform, and slog.
"""

import os
import sys
import argparse

def scaffold_go(module_name: str, out_dir: str):
    os.makedirs(os.path.join(out_dir, "cmd", "server"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "internal", "platform", "logger"), exist_ok=True)

    # go.mod
    with open(os.path.join(out_dir, "go.mod"), "w") as f:
        f.write(f"module {module_name}\n\ngo 1.23\n")

    # main.go
    main_go = f"""package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"{module_name}/internal/platform/logger"
)

func main() {{
	log := logger.InitLogger(os.Getenv("ENV") == "production")
	log.Info("Starting server", "module", "{module_name}")

	mux := http.NewServeMux()
	mux.HandleFunc("GET /healthz", func(w http.ResponseWriter, r *http.Request) {{
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}})

	srv := &http.Server{{
		Addr:         ":8080",
		Handler:      mux,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
	}}

	go func() {{
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {{
			log.Error("server error", "err", err)
			os.Exit(1)
		}}
	}}()

	// Graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {{
		log.Error("shutdown error", "err", err)
	}}
	log.Info("Server stopped cleanly")
}}
"""
    with open(os.path.join(out_dir, "cmd", "server", "main.go"), "w") as f:
        f.write(main_go)

    # logger.go
    logger_go = """package logger

import (
	"log/slog"
	"os"
)

func InitLogger(isProd bool) *slog.Logger {
	var h slog.Handler
	if isProd {
		h = slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo})
	} else {
		h = slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelDebug})
	}
	l := slog.New(h)
	slog.SetDefault(l)
	return l
}
"""
    with open(os.path.join(out_dir, "internal", "platform", "logger", "logger.go"), "w") as f:
        f.write(logger_go)

    print(f" Scaffolded Go service '{module_name}' at {out_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", required=True, help="Go module name (e.g. github.com/user/service)")
    parser.add_argument("--out", default=".", help="Target directory")
    args = parser.parse_args()
    scaffold_go(args.module, args.out)
