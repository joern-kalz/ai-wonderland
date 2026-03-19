export default function LoadingSpinner() {
    return (
        <div className="absolute inset-0 flex items-center justify-center bg-black opacity-30">
            <div className="h-32 w-32 animate-spin rounded-full border-b-2 border-t-2 border-white"></div>
        </div>
    );
}
